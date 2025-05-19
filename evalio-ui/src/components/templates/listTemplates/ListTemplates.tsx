import { useNavigate, useParams } from 'react-router';
// import templates from './../mockTemplates.json';
import './listTemplates.css';
import Navbar from '../../navbar/navbar';
import { useEffect, useState } from 'react';
import { getTemplatesByGroup } from '../../../services/manager/managerService';
import type { Template } from '../../../services/manager/entities/templates';
const ListTemplates = () => {
  const { id } = useParams<{ id: string }>();

  const navigate = useNavigate();

  const handleCreateTemplate = (groupId: string | undefined) => {
    if (groupId) {
      navigate(`/template/group/${groupId}`);
    }
  };

  const handleCardClick = (id: string) => {
    navigate(`/template/${id}`);
  };
  const [templates, setTemplates] = useState<Template[]>([]);
  useEffect(() => {
    if (id) {
      getTemplatesByGroup(id).then((data) => {
        setTemplates(data);
      });
    }
    return () => {};
  }, [id]);

  return (
    <>
      <Navbar></Navbar>
      <div>
        <div className='templates-header'>
          <h4>Plantillas de parciales</h4>
          <h5>Escoja su plantilla para ver la información detallada</h5>
          <button onClick={() => handleCreateTemplate(id)}>
            Registrar plantilla
          </button>
        </div>
        <div className='container-templates'>
          {templates.map((template) => {
            return (
              <div
                key={template.id}
                className='card-group'
                onClick={() => handleCardClick(template.id)}
              >
                <h5>
                  {' '}
                  Materia <strong>{template.subject_name} </strong>{' '}
                </h5>
                <h5>
                  {' '}
                  Periodo <strong>{template.period}</strong>
                </h5>
                <h5>
                  {' '}
                  Corte <strong># {template.number}</strong>
                </h5>
                <h5>
                  {' '}
                  Cantidad de preguntas{' '}
                  <strong>{template.questions.length}</strong>
                </h5>
              </div>
            );
          })}
        </div>
      </div>
    </>
  );
};

export default ListTemplates;
