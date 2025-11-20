import React from 'react';
import { useParams } from 'react-router-dom';
import useTemplate from '@/features/groups/hooks/useTemplate';
import { useNavigate } from 'react-router-dom';
import styles from './templateDetail.module.scss';
import BackButton from '@/shared/components/BackButton/BackButton';

const TemplateDetail: React.FC = () => {
  const { id } = useParams();
  const { groupId } = useParams();
  const { data: template, status, error } = useTemplate(id);
  const navigate = useNavigate();

  if (status === 'pending') return <div className={styles.container}>Cargando...</div>;
  if (status === 'error') return <div className={styles.container}>Error: {(error as Error)?.message}</div>;
  if (!template) return <div className={styles.container}>Plantilla no encontrada</div>;

  return (
    <div className={styles.container}>
      <div className={styles.grid}>
        <div className={styles.left}>
          <header className={styles.header}>
          <div className={styles.backWrapper}>
            <BackButton onClick={() => navigate(`/group/${groupId || template.group_id}`)} />
          </div>
            <h2>Hoja de Respuestas</h2>
            <div className={styles.meta}>
              <div>Materia: <strong>{template.subject_name}</strong></div>
              <div>Periodo: <strong>{template.period}</strong></div>
              <div>Corte: <strong>{template.number}</strong></div>
            </div>
          </header>

          <div className={styles.sheet} aria-label="Hoja de respuestas">
            {template.questions.map((q) => (
              <div key={q.question} className={styles.questionRow}>
                <div className={styles.index}>{q.question}.</div>
                <div className={styles.options}>
                  {['A', 'B', 'C', 'D'].map((opt) => (
                    <div
                      key={opt}
                      className={
                        opt === q.answer ? `${styles.option} ${styles.selected}` : styles.option
                      }
                      aria-checked={opt === q.answer}
                    >
                      <span className={styles.circle} />
                      <span className={styles.optLabel}>{opt}</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className={styles.right}>
          {/* Actions placeholder - reserved for future controls */}
          <div />
        </div>
      </div>
    </div>
  );
};

export default TemplateDetail;
