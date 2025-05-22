import { useEffect, useState } from 'react';
import Navbar from '../../navbar/navbar';
import './listGroup.css';
import { useNavigate } from 'react-router';
import CreateGroup from '../createGroup/CreateGroup';
import {
  deleteGroupById,
  getGroupsByProfessor,
} from '../../../services/manager/managerService';
import type { Groups } from '../../../services/manager/entities/groups';
import deleteICon from '../../../assets/icons8-delete.svg';
const ListGroup = () => {
  const navigate = useNavigate();
  const [groups, setGroups] = useState<Groups[]>([]);
  const [reload, setReload] = useState<string>('');
  const handleOpenGroup = (id: string) => {
    navigate(`/group/${id}`);
  };
  const [isOpenCreateGroup, setIsOpenCreateGroup] = useState<boolean>(false);
  const handleCreateGroup = () => {
    setIsOpenCreateGroup(true);
  };

  useEffect(() => {
    getGroupsByProfessor().then((data) => {
      setGroups([...data]);
    });
    return () => {};
  }, [reload]);

  const handleDeleteGroup = (groupId: string) => {
    deleteGroupById(groupId).then();
    const newGroups = groups.filter((data) => data.id != groupId);
    setGroups([...newGroups]);
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
                <div key={group.id}>
                  <div
                    className='card-group'
                    onClick={() => handleOpenGroup(group.id)}
                  >
                    <h5>
                      <strong>{group.subject_name} </strong>
                    </h5>
                    <h5>{group.name}</h5>

                    <h5>
                      Periodo académico: <strong>{group.period}</strong>
                    </h5>
                  </div>
                  <img
                    onClick={() => handleDeleteGroup(group.id)}
                    src={deleteICon}
                  ></img>
                </div>
              );
            })}
          </div>
        )}
        {isOpenCreateGroup && (
          <CreateGroup
            setIsOpenCreateGroup={setIsOpenCreateGroup}
            setReload={setReload}
          ></CreateGroup>
        )}
      </div>
    </>
  );
};

export default ListGroup;
