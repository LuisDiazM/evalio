import { useState } from 'react';
import Navbar from '../../navbar/navbar';
import './listGroup.css';
import groups from './mockGroups.json';
import { useNavigate } from 'react-router';
import CreateGroup from '../createGroup/CreateGroup';
const parseDate = (date: string) => {
  try {
    const locaDate = new Date(date).toLocaleString('es-ES');
    return locaDate.slice(1);
  } catch {
    return '';
  }
};

const ListGroup = () => {
  const navigate = useNavigate();
  const handleOpenGroup = (id: string) => {
    navigate(`/group/${id}`);
  };
  const [isOpenCreateGroup, setIsOpenCreateGroup] = useState<boolean>(false);
  const handleCreateGroup = () => {
    setIsOpenCreateGroup(true);
  };
  return (
    <>
      <Navbar></Navbar>
      <div className='container-list-group'>
        <div className='groups-header'>
          <h3>Grupos</h3>
          <h5>Escoja el grupo para ver su información detallada</h5>
          {!isOpenCreateGroup && (
            <button onClick={() => handleCreateGroup()}>Registrar grupo</button>
          )}
        </div>
        {!isOpenCreateGroup && (
          <div className='container-groups'>
            {groups.map((group) => {
              return (
                <div
                  key={group.id}
                  className='card-group'
                  onClick={() => handleOpenGroup(group.id)}
                >
                  <h5>
                    <strong>{group.subject_name} </strong>
                  </h5>
                  <h5>{group.name}</h5>
                  <h5>
                    Fecha creación{' '}
                    <strong>{parseDate(group.created_at)} </strong>
                  </h5>
                  <h5>
                    Periodo académico: <strong>{group.period}</strong>
                  </h5>
                </div>
              );
            })}
          </div>
        )}
        {isOpenCreateGroup && (
          <CreateGroup
            setIsOpenCreateGroup={setIsOpenCreateGroup}
          ></CreateGroup>
        )}
      </div>
    </>
  );
};

export default ListGroup;
