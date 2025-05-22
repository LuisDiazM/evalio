import Navbar from '../../navbar/navbar';
import { useState, useRef } from 'react';
import { Scanner } from '@yudiel/react-qr-scanner';
import Webcam from 'react-webcam';
import './uploadEvaluation.css';
import { base64ToFile } from './base64Transformation';
const UploadEvaluation = () => {
  const [step, setStep] = useState(1);
  const [qrResult, setQrResult] = useState<string | null>(null);
  const [image, setImage] = useState<string | null>(null);
  const webcamRef = useRef<Webcam>(null);

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
    } catch (error) {
      alert('El código QR no contiene datos válidos.');
      setQrResult(null);
    }
  };

  const handleCapture = () => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      setImage(imageSrc);
      const file = base64ToFile(imageSrc, 'output.png');
      console.log(file);
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
              styles={{ container: { height: '60%', width: '60%' } }}
              onScan={handleQrScan}
              videoConstraints={{ facingMode: 'environment' }}
              onError={(error) => alert(`Error: ${error.message}`)}
            />
            {qrResult && <p>Código QR detectado: {qrResult}</p>}
          </div>
        )}
        {step === 2 && image == null && (
          <div className='camera-window'>
            <h2>Capturar Hoja de Respuestas</h2>
            <p>Alinea la hoja de respuestas dentro del marco rojo</p>
            <div
              style={{
                position: 'relative',
                width: '400px',
                height: '720px',
              }}
            >
              <Webcam
                audio={false}
                height={720}
                width={400}
                screenshotFormat='image/jpeg'
                videoConstraints={{
                  width: 400,
                  height: 720,
                  facingMode: 'environment',
                }}
                ref={webcamRef}
              />
              <div
                style={{
                  position: 'absolute',
                  top: '10%',
                  left: '10%',
                  width: '80%',
                  height: '80%',
                  border: '2px solid red',
                  boxSizing: 'border-box',
                }}
              />
            </div>
            <button className='camera-button' onClick={handleCapture}></button>
          </div>
        )}

        {image && (
          <div className='photo-scan'>
            <h3>Imagen Capturada</h3>
            <img
              src={image}
              alt='Hoja capturada'
              style={{ maxWidth: '100%' }}
            />
            <button>Enviar</button>
          </div>
        )}
      </div>
    </>
  );
};

export default UploadEvaluation;
