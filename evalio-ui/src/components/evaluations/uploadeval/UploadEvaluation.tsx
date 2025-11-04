import Navbar from '../../navbar/navbar';
import { useState, useRef } from 'react';
import { Scanner } from '@yudiel/react-qr-scanner';
import Webcam from 'react-webcam';
import './uploadEvaluation.css';
import { base64ToFile } from './base64Transformation';
import { uploadExam } from '../../../services/manager/managerService';

const UploadEvaluation = () => {
  const [step, setStep] = useState(1);
  const [qrResult, setQrResult] = useState<any>(null);
  const [image, setImage] = useState(null);
  const [aspectRatio, setAspectRatio] = useState(1); // Estado para la relación de aspecto
  const webcamRef:any = useRef(null);

  const videConstrains = {
    facingMode: 'environment',
    width: { ideal: 1920 }, // Restauramos resolución alta
    height: { ideal: 1920 },
  };

  const handleQrScan = (result:any) => {
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
      const imageSrc = webcamRef.current?.getScreenshot({
        width: 1920, // Forzamos el ancho de la captura
        height: 1920 * aspectRatio, // Ajustamos la altura según la relación de aspecto
        screenshotQuality: 1, // Máxima calidad (0 a 1)
      });
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

  // Función para obtener las dimensiones del video y ajustar la relación de aspecto
  const handleUserMedia = (stream:any) => {
    const track = stream.getVideoTracks()[0];
    const settings = track.getSettings();
    if (settings.width && settings.height) {
      const ratio = settings.height / settings.width;
      setAspectRatio(ratio);
    }
  };

  return (
    <>
      <Navbar />
      <div style={{ textAlign: 'center', padding: '20px' }}>
        {step === 1 && (
          <div className="camera-window">
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
          <div className="camera-window">
            {/* Contenedor con relación de aspecto dinámica */}
            <div
              style={{
                position: 'relative',
                width: '100%',
                paddingTop: `${aspectRatio * 100}%`, // Ajusta la altura según la relación de aspecto
                maxHeight: '70vh', // Limita la altura máxima
                overflow: 'hidden', // Evita desbordamientos
              }}
            >
              <Webcam
                key={step}
                audio={false}
                screenshotFormat="image/jpeg"
                videoConstraints={{ ...videConstrains }}
                ref={webcamRef}
                onUserMedia={handleUserMedia} // Detecta las dimensiones del video
                style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  width: '100%',
                  height: '100%',
                  objectFit: 'cover',
                }}
              />
            </div>
            <button className="camera-button" onClick={handleCapture}></button>
          </div>
        )}
        {image && (
          <div className="photo-scan">
            <h3>Imagen Capturada</h3>
            <img
              src={image}
              alt="Hoja capturada"
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