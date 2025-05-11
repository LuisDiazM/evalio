import { useNavigate } from 'react-router';
import templates from './../mockTemplates.json';
import './listTemplates.css';
import Navbar from '../../navbar/navbar';
const ListTemplates = () => {
  const navigate = useNavigate();

  const handleCardClick = (id: string) => {
    navigate(`/template/${id}`);
  };

  return (
    <>
      <Navbar></Navbar>
      <div>
        <div className='templates-header'>
          <h4>Plantillas de parciales</h4>
          <h5>Escoja su plantilla para ver la información detallada</h5>
          <button>Registrar plantilla</button>
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
