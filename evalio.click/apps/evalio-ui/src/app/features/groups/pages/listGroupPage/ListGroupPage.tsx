import React from 'react';
import { useNavigate } from 'react-router-dom';
import styles from '@/features/groups/pages/listGroupPage/listGroupPage.module.scss';
import useGroups from '@/features/groups/hooks/useGroups';
import { Group } from '@/features/groups/services/groups.service';
import DeleteGroupButton from '@/features/groups/components/deleteGroup/DeleteGroupButton';


const ListGroupPage: React.FC = () => {
  const { data: groups, isLoading, isError, error } = useGroups();
  const navigate = useNavigate();

  const handleCreate = () => {
    navigate('/group/create');
  };

  return (
    <div className={styles.container as string}>
      <div className={styles.headerComponent as string}>
        <h2>Listado de grupos</h2>
        <button onClick={handleCreate}>
          Crear grupo
        </button>
      </div>

      {isLoading && <p>Cargando grupos...</p>}
      {isError && <p>Error al cargar grupos: {String(error)}</p>}

      {!isLoading && !isError && (
        <div className={styles.tableWrapper as string}>
          <table className={styles.table as string} aria-label="Lista de grupos">
            <thead>
              <tr>
                <th>Materia</th>
                <th>Periodo académico</th>
                <th>Cantidad de estudiantes</th>
                <th>Nombre del grupo</th>
                <th>Eliminar</th>
              </tr>
            </thead>
            <tbody>
              {(groups || []).map((g: Group) => (
                <tr
                  key={g?.id}
                  role="button"
                  tabIndex={0}
                  onClick={() => navigate(`/group/${g.id}`)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' || e.key === ' ') navigate(`/group/${g.id}`);
                  }}
                  style={{ cursor: 'pointer' }}
                >
                  <td>{g?.subject_name}</td>
                  <td>{g?.period}</td>
                  <td>{g?.students ? g.students.length : 0}</td>
                  <td>{g?.name}</td>
                  <td onClick={(e) => e.stopPropagation()}>
                    <DeleteGroupButton groupId={g.id} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default ListGroupPage;
