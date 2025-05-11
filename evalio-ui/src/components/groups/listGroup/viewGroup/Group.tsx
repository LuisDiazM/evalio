import './group.css';
import groups from '../mockGroups.json';
import { useNavigate, useParams } from 'react-router';
import Navbar from '../../../navbar/navbar';

// interface GroupProps {
//   group: {
//     id: string;
//     subject_name: string;
//     name: string;
//     created_at: string;
//     period: string;
//     students: {
//       name: string;
//       identification: number;
//     }[];
//   };
// }

const Group = () => {
  const group = groups[0];
  const { id } = useParams<{ id: string }>();
  console.log(id);
  const navigate = useNavigate();
  const handleTemplates = (id: string | undefined) => {
    if (id) {
      navigate(`/group/${id}/templates`);
    }
  };

  return (
    <>
      {' '}
      <Navbar></Navbar>
      <div className='group-container'>
        <div>
          <h5>
            <strong>{group.subject_name}</strong>
          </h5>
          <h5>
            Fecha creación <strong>{group.created_at} </strong>
          </h5>
          <h5>
            Periodo académico: <strong>{group.period}</strong>
          </h5>
          <h5>{group.name}</h5>

          <div className='settings-group'>
            <button onClick={() => handleTemplates(id)}>Ver parciales</button>
            <button>Ver calificaciones</button>
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
              {group.students.map((student) => (
                <tr key={student.identification}>
                  <td>{student.identification}</td>
                  <td>{student.name}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
};

export default Group;
