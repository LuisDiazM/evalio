import React, { useCallback, useState } from 'react';
import styles from './qualificationsList.module.scss';
import useSummary from '@/features/groups/hooks/useSummary';
import ExportCSVButton from '@/features/groups/components/ExportCSVButton/ExportCSVButton';
import ModalImageViewer from './ModalImageViewer';

type Props = { groupId?: string; templateId?: string };

const QualificationsList: React.FC<Props> = ({ groupId, templateId }) => {
  const { data, status, error } = useSummary(templateId);

  const [selectedImage, setSelectedImage] = useState<string | null>(null);

  const resolveUrl = useCallback((path?: string) => {
    if (!path) return null;
    return path.startsWith('http') ? path : `${window.location.origin}/${path}`;
  }, []);

  const openExam = (path?: string) => {
    const url = resolveUrl(path);
    if (!url) return;
    setSelectedImage(url);
  };

  const closeModal = useCallback(() => setSelectedImage(null), []);

  // modal behavior is handled by ModalImageViewer

  if (!templateId) return <div className={styles.container}>No template selected</div>;
  if (status === 'pending') return <div className={styles.container}>Cargando resumen...</div>;
  if (status === 'error') return <div className={styles.container}>Error: {(error as Error)?.message}</div>;
  if (!data || !data.students || data.students.length === 0) return <div className={styles.container}>No hay calificaciones</div>;

  // only show export when there is valid data and templateId
  const showExport = Boolean(templateId && data && data.students && data.students.length > 0);

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        {showExport && (
          <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: 8 }}>
            <ExportCSVButton templateId={String(templateId)} />
          </div>
        )}
        <table className={styles.table}>
          <thead>
            <tr>
              <th>Identificación</th>
              <th>Nombre</th>
              <th>Calificación</th>
              <th>Ver</th>
            </tr>
          </thead>
          <tbody>
            {data.students.map((s, i) => (
              <tr key={`${s.student_identification}-${i}`}>
                <td>{s.student_identification}</td>
                <td>{String(s.student_name || '').trim()}</td>
                <td>{s.score}</td>
                <td>
                  <button
                    className={styles.viewBtn}
                    aria-label={`Ver examen ${s.student_identification}`}
                    onClick={() => openExam(s.exam_path)}
                    title="Ver examen"
                  >
                    <span role="img" aria-hidden="true" className={styles.icon}>
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                        <circle cx="12" cy="12" r="3"></circle>
                      </svg>
                    </span>
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {selectedImage && (
        <ModalImageViewer
          src={selectedImage}
          alt="Examen"
          onClose={closeModal}
        />
      )}
    </div>
  );
};

export default QualificationsList;
