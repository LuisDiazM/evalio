import { useRef, useState, useCallback } from 'react';
import { base64ToFile } from '../../utils/base64transformation';
import { uploadExam } from '../../services/evaluation.service';
import Webcam from 'react-webcam';
import { Scanner } from '@yudiel/react-qr-scanner';
import styles from './uploadExam.module.scss';

type QrPayload = {
  group_id: string;
  student_id: string | number;
  template_response_id: string;
  student_name?: string;
};

const UploadExamPage: React.FC = () => {
  const [step, setStep] = useState<number>(1);
  const [qrResult, setQrResult] = useState<QrPayload | null>(null);
  const [image, setImage] = useState<string | null>(null);
  const [aspectRatio, setAspectRatio] = useState<number>(1);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const webcamRef = useRef<Webcam | null>(null);

  const videoConstraints = {
    facingMode: 'environment',
    width: { ideal: 1920 },
    height: { ideal: 1920 },
  } as const;

  const handleQrScan = useCallback((result: unknown) => {
    // scanner returns an array of results; guard carefully
    const arr = result as unknown[] | undefined;
    if (!arr || !Array.isArray(arr) || arr.length === 0) return;
    const first = arr[0] as { rawValue?: unknown } | undefined;
    if (!first || typeof first.rawValue !== 'string') return;

    try {
      const qrData = first.rawValue as string;
      let parsed: unknown;
      try {
        parsed = JSON.parse(qrData);
      } catch {
        // some scanners return single-quoted JSON; try to fix
        const fixedJson = qrData.replace(/'/g, '"');
        parsed = JSON.parse(fixedJson);
      }

      setQrResult(parsed as QrPayload);
      setStep(2);
      setError(null);
    } catch (e) {
      console.error('QR parse error', e);
      setQrResult(null);
      setStep(1);
      setError('QR inválido');
    }
  }, []);

  const handleUserMedia = useCallback((stream: MediaStream) => {
    const track = stream.getVideoTracks()?.[0];
    const settings = track?.getSettings();
    if (settings?.width && settings?.height) {
      const ratio = settings.height / settings.width;
      setAspectRatio(ratio);
    }
  }, []);

  const handleCapture = useCallback(() => {
    if (!webcamRef.current) return;
    // react-webcam's getScreenshot method type can be narrowed safely
    const cam = webcamRef.current as unknown as {
      getScreenshot?: (opts?: { width?: number; height?: number }) => string | null;
    } | null;
    const imageSrc = cam?.getScreenshot?.({
      width: 1920,
      height: Math.max(480, Math.round(1920 * aspectRatio)),
    }) ?? null;
    if (imageSrc) setImage(imageSrc as string);
  }, [aspectRatio]);

  const resetStatus = useCallback(() => {
    setQrResult(null);
    setImage(null);
    setStep(1);
    setError(null);
  }, []);

  const makeFilename = useCallback((payload: QrPayload) => {
    return `exam-${payload.template_response_id}-${payload.student_id}.jpeg`;
  }, []);

  const handleUploadExam = useCallback(async () => {
    if (!qrResult || !image) return;
    setLoading(true);
    setError(null);

    try {
      const file = base64ToFile(image, makeFilename(qrResult));
      if (!file) throw new Error('No se pudo procesar la imagen');

      const formData = new FormData();
      formData.append('file', file);
      formData.append('group_id', String(qrResult.group_id));
      formData.append('student_id', String(qrResult.student_id));
      formData.append('template_response_id', String(qrResult.template_response_id));
      if (qrResult.student_name) formData.append('student_name', qrResult.student_name);

      await uploadExam(formData);
      resetStatus();
    } catch (e) {
      console.error('Upload error', e);
      setError('Error al subir el examen');
    } finally {
      setLoading(false);
    }
  }, [qrResult, image, makeFilename, resetStatus]);

  return (
    <div className={styles.wrapper}>
      <div className={styles.container}>
        {step === 1 && (
          <section className={styles.scanner}>
            <h2>Escanear Código QR</h2>
            <p>Centra el código QR en la pantalla</p>
            <Scanner
              key={step}
              styles={{ container: { height: '80%', width: '80%' } }}
              onScan={handleQrScan}
              constraints={videoConstraints}
              onError={(err) => setError(String(err))}
            />
            {error && <div className={styles.error}>{error}</div>}
          </section>
        )}

        {step === 2 && !image && (
          <section className={styles.cameraStage}>
            <div className={styles.cameraContainer} style={{ paddingTop: `${Math.round(aspectRatio * 100)}%` }}>
              <Webcam
                key={step}
                audio={false}
                screenshotFormat="image/jpeg"
                videoConstraints={{ ...videoConstraints }}
                ref={webcamRef}
                onUserMedia={handleUserMedia}
                className={styles.webcam}
              />
            </div>
            <button className={styles.cameraButton} onClick={handleCapture} aria-label="Tomar foto" />
          </section>
        )}

        {image && (
          <section className={styles.preview}>
            <h3>Imagen Capturada</h3>
            <img src={image} alt="Hoja capturada" className={styles.previewImage} />
            <div className={styles.actions}>
              <button onClick={resetStatus} disabled={loading} className={styles.secondary}>
                Volver
              </button>
              <button onClick={handleUploadExam} disabled={loading} className={styles.primary}>
                {loading ? 'Enviando...' : 'Enviar'}
              </button>
            </div>
            {error && <div className={styles.error}>{error}</div>}
          </section>
        )}
      </div>
    </div>
  );
};

export default UploadExamPage;
