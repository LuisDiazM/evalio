import { useNavigate } from 'react-router';
import './listTemplates.css';
import { useEffect, useState } from 'react';
import {
  deleteTemplateById,
  getTemplatesByGroup,
} from '../../../services/manager/managerService';
import type { Template } from '../../../services/manager/entities/templates';
import deleteICon from '../../../assets/icons8-delete.svg';

interface ListTemplatesProps {
  id: string | undefined;
}

const ListTemplates = ({ id }: ListTemplatesProps) => {
  // const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

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

  const handleDeleteTemplate = (templateId: string) => {
    deleteTemplateById(templateId).then();
    const filterTemplates = templates.filter((data) => data.id != templateId);
    setTemplates([...filterTemplates]);
  };

  return (
    <>
      <div>
        <div className='templates-header'>
          <h5>
            {' '}
            <strong>Mis parciales </strong>
          </h5>
        </div>
        <div className='container-templates'>
          {templates.map((template) => {
            return (
              <div key={template.id}>
                <div
                  className='card-group'
                  onClick={() => handleCardClick(template.id)}
                >
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
                <img
                  onClick={() => handleDeleteTemplate(template.id)}
                  src={deleteICon}
                ></img>
              </div>
            );
          })}
        </div>
      </div>
    </>
  );
};

export default ListTemplates;
