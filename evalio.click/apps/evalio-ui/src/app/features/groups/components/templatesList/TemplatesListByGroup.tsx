import React from 'react';
import { useNavigate } from 'react-router-dom';
import useTemplatesByGroup from '@/features/groups/hooks/useTemplatesByGroup';
import styles from './templatesList.module.scss';
import { formatDate } from '@/shared/functions/formatDate';

type Props = { groupId?: string };

const TemplatesListByGroup: React.FC<Props> = ({ groupId }) => {
  const navigate = useNavigate();
  const { data: templates, status, error } = useTemplatesByGroup(groupId);



  if (!groupId)
    return <div className={styles.container}>No group selected</div>;
  if (status === 'pending')
    return <div className={styles.container}>Cargando plantillas...</div>;
  if (status === 'error')
    return (
      <div className={styles.container}>Error: {(error as Error)?.message}</div>
    );
  if (!templates || templates?.length === 0) {
    return (
      <div className={styles.container}>
        No hay plantillas disponibles para este grupo
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <h3>Plantillas</h3>
      <div className={styles.card}>
        <table className={styles.table}>
          <thead>
            <tr>
              <th>Cantidad de preguntas</th>
              <th>Creado</th>
              <th>Corte</th>
            </tr>
          </thead>
          <tbody>
            {(templates || []).map((t) => (
              <tr
                key={t.id}
                role="button"
                tabIndex={0}
                onClick={() => navigate(`/group/${groupId}/template/${t.id}`)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ')
                    navigate(`/group/${groupId}/template/${t.id}`);
                }}
                style={{ cursor: 'pointer' }}
              >
                <td>{t.questions?.length ?? 0}</td>
                <td>{formatDate(t.created_at)}</td>
                <td> {t.number}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TemplatesListByGroup;
