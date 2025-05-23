import './group.css';
import { useNavigate, useParams } from 'react-router';
import Navbar from '../../navbar/navbar';
import { useEffect, useState } from 'react';
import { getGroupById } from '../../../services/manager/managerService';
import type { Groups } from '../../../services/manager/entities/groups';
import ListTemplates from '../../templates/listTemplates/ListTemplates';

const Group = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [group, setGroup] = useState<Groups | null>(null);
  useEffect(() => {
    if (id) {
      getGroupById(id).then((data) => {
        if (data != null) {
          setGroup(data);
        }
      });
    }

    return () => {};
  }, [id]);
  const handleCreateTemplate = (groupId: string | undefined) => {
    if (groupId) {
      navigate(`/template/group/${groupId}`);
    }
  };
  return (
    <>
      {' '}
      <Navbar></Navbar>
      {group != null && (
        <div className='group-container'>
          <div>
            <h5>
              Materia: <strong>{group?.subject_name}</strong>
            </h5>

            <h5>
              Periodo académico: <strong>{group?.period}</strong>
            </h5>
            <h5>
              Grupo: <strong>{group?.name} </strong>{' '}
            </h5>
            
            <ListTemplates id={id}></ListTemplates>
            <div className='settings-group'>
              <button onClick={() => handleCreateTemplate(id)}>
                Registrar plantilla respuestas
              </button>
            </div>
          </div>

          <div>
            <table>
              <thead>
                <tr>
                  <th>Identificación</th>
                  <th>Nombre</th>
                </tr>
              </thead>
              <tbody>
                {group?.students.map((student) => (
                  <tr key={student.identification}>
                    <td>{student.identification}</td>
                    <td>{student.name}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </>
  );
};

export default Group;
