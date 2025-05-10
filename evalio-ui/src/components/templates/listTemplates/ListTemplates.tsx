import { useNavigate } from 'react-router';
import templates from './../mockTemplates.json';
import './listTemplates.css';
const ListTemplates = () => {
  const navigate = useNavigate();

  const handleCardClick = (id: string) => {
    navigate(`/template/${id}`);
  };

  return (
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
              Cantidad de preguntas <strong>{template.questions.length}</strong>
            </h5>
          </div>
        );
      })}
    </div>
  );
};

export default ListTemplates;
