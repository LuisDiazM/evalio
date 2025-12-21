import type { Student } from '@/features/groups/services/groups.service';
import { useParams } from 'react-router-dom';
import useGroup from '@/features/groups/hooks/useGroup';
import styles from './groupDetail.module.scss';
import TemplatesListByGroup from '@/features/groups/components/templatesList/TemplatesListByGroup';
import CreateTemplate from '@/features/groups/pages/createTemplate/CreateTemplate';
import { useState } from 'react';
import BackButton from '@/shared/components/BackButton/BackButton';
import { useNavigate } from 'react-router-dom';

export const GroupDetailPage = () => {
  const { id } = useParams();
  const { data: group, status, error } = useGroup(id);
  const navigate = useNavigate();
  const [creating, setCreating] = useState(false);

  if (status === 'pending') return <div className={styles.container}>Cargando...</div>;
  if (status === 'error') return <div className={styles.container}>Error: {(error as Error)?.message}</div>;

  if (!group) return <div className={styles.container}>Grupo no encontrado</div>;

  return (
    <div className={styles.container}>
      <header className={styles.heading}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <BackButton onClick={() => navigate('/groups')} />
          <h1>{group?.name}</h1>
        </div>
        <div className={styles.meta}>
          Profesor: {group?.professor_name} | Materia: {group.subject_name}
        </div>
      </header>

      <div className={styles.grid}>
        <div>
          <section className={styles.studentsCard}>
            <h3>Listado de estudiantes</h3>
            {group?.students && group?.students.length ? (
              <table className={styles.studentsTable}>
                <thead>
                  <tr>
                    <th>Nombre</th>
                    <th>Documento</th>
                  </tr>
                </thead>
                <tbody>
                  {group?.students.map((s: Student, i: number) => (
                    <tr key={i}>
                      <td>{s?.name}</td>
                      <td>{s?.identification}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <div className={styles.empty}>No hay estudiantes registrados</div>
            )}
          </section>
        </div>

        <div>
          {!creating && (
            <div className={styles.createBtnRow}>
              <button onClick={() => setCreating(true)}>Crear plantilla</button>
            </div>
          )}

          {creating ? (
            <CreateTemplate
              group_id={group?.id}
              period={group?.period}
              subject_name={group?.subject_name}
              onCancel={() => setCreating(false)}
              onCreated={() => setCreating(false)}
            />
          ) : (
            <TemplatesListByGroup groupId={group?.id} />
          )}
        </div>
      </div>
    </div>
  );
};

export default GroupDetailPage;
