import './listGroup.css';
import groups from './mockGroups.json';
import { useNavigate } from 'react-router';

const ListGroup = () => {
  const parseDate = (date: string) => {
    try {
      const locaDate = new Date(date).toLocaleString('es-ES');
      return locaDate.slice(1);
    } catch {
      return '';
    }
  };

  const navigate = useNavigate();
  const handleClick = (id: string) => {
    navigate(`/group/${id}`);
  };
  return (
    <>
      <div className='container'>
        {groups.map((group) => {
          return (
            <div className='card-group' onClick={() => handleClick(group.id)}>
              <h5>
                <strong>{group.subject_name} </strong>
              </h5>
              <h5>{group.name}</h5>
              <h5>
                Fecha creación <strong>{parseDate(group.created_at)} </strong>
              </h5>
              <h5>
                Periodo académico: <strong>{group.period}</strong>
              </h5>
            </div>
          );
        })}
      </div>
    </>
  );
};

export default ListGroup;
