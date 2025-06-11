import Navbar from '../../navbar/navbar';
import { useState, useRef } from 'react';
import { Scanner } from '@yudiel/react-qr-scanner';
import Webcam from 'react-webcam';
import './uploadEvaluation.css';
import { base64ToFile } from './base64Transformation';
import { uploadExam } from '../../../services/manager/managerService';
const UploadEvaluation = () => {
  const [step, setStep] = useState(2);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [qrResult, setQrResult] = useState<any | null>(null);
  const [image, setImage] = useState<string | null>(null);
  const webcamRef = useRef<Webcam>(null);
  const videConstrains = {
    facingMode: 'environment',
    width: { ideal: 1920 },
    height: { ideal: 1920 },
  };
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const handleQrScan = (result: string | any[]) => {
    if (!result || !Array.isArray(result) || !result[0]?.rawValue) return;

    try {
      const qrData = result[0].rawValue;
      let parsed;
      try {
        parsed = JSON.parse(qrData);
      } catch {
        const fixedJson = qrData.replace(/'/g, '"');
        parsed = JSON.parse(fixedJson);
      }
      setQrResult(parsed);
      setStep(2);
    } catch {
      setQrResult(null);
      setStep(1);
    }
  };

  const handleCapture = () => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      setImage(imageSrc);
    }
  };

  const resetStatus = () => {
    setQrResult(null);
    setImage(null);
    setStep(1);
  };

  const handleUploadExam = () => {
    const formData = new FormData();
    if (qrResult) {
      const file = base64ToFile(
        image,
        `exam-${qrResult?.template_response_id}-${qrResult?.student_id}.jpeg`
      );
      if (file) {
        formData.append('file', file);
        formData.append('group_id', qrResult?.group_id);
        formData.append('student_id', qrResult?.student_id);
        formData.append('template_response_id', qrResult?.template_response_id);
        formData.append('student_name', qrResult?.student_name);

        uploadExam(formData)
          .then(() => {
            resetStatus();
          })
          .catch(() => {
            resetStatus();
          });
      }
    }
  };

  return (
    <>
      <Navbar></Navbar>
      <div style={{ textAlign: 'center', padding: '20px' }}>
        {step === 1 && (
          <div className='camera-window'>
            <h2>Escanear Código QR</h2>
            <p>Centra el código QR en la pantalla</p>
            <Scanner
              key={step}
              styles={{ container: { height: '80%', width: '80%' } }}
              onScan={handleQrScan}
              constraints={videConstrains}
              onError={(error) => alert(`Error: ${error}`)}
            />
          </div>
        )}
        {step === 2 && image == null && (
          <div className='camera-window'>
            <Webcam
              key={step}
              audio={false}
              screenshotFormat='image/jpeg'
              videoConstraints={{...videConstrains}}
              ref={webcamRef}
              style={{
                width: '100%',
                height: '70vh',
                objectFit: 'cover',
              }}
            />
            <button className='camera-button' onClick={handleCapture}></button>
          </div>
        )}

        {image && (
          <div className='photo-scan'>
            <h3>Imagen Capturada</h3>
            <img
              src={image}
              alt='Hoja capturada'
              style={{ maxWidth: '100%', maxHeight: '100%' }}
            />
            <button onClick={() => handleUploadExam()}>Enviar</button>
          </div>
        )}
      </div>
    </>
  );
};

export default UploadEvaluation;
