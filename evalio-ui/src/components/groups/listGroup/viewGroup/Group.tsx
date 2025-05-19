import './group.css';
import { useNavigate, useParams } from 'react-router';
import Navbar from '../../../navbar/navbar';
import { useEffect, useState } from 'react';
import { getGroupById } from '../../../../services/manager/managerService';
import type { Groups } from '../../../../services/manager/entities/groups';

const Group = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const handleTemplates = (id: string | undefined) => {
    if (id) {
      navigate(`/group/${id}/templates`);
    }
  };
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

  return (
    <>
      {' '}
      <Navbar></Navbar>
      {group != null && (
        <div className='group-container'>
          <div>
            <h5>
              <strong>{group?.subject_name}</strong>
            </h5>

            <h5>
              Periodo académico: <strong>{group?.period}</strong>
            </h5>
            <h5>{group?.name}</h5>

            <div className='settings-group'>
              <button onClick={() => handleTemplates(id)}>Ver parciales</button>
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
