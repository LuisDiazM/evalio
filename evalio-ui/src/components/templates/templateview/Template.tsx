import templates from '../mockTemplates.json';
import './template.css';

import { useParams } from 'react-router';

const Template = () => {
  const template = templates[0];

  const { id } = useParams<{ id: string }>();

  return (
    <div className='container-template'>
      <div key={template.id}>
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
      <div className='questions-list'>
        {template.questions.map((question, index) => {
          return (
            <div key={`${id}-${index}`} className='container-responses'>
              <div className='question-number'> {question.question} </div>
              <div
                style={{
                  backgroundColor:
                    question.answer == 'A' ? '#a5f390' : 'transparent',
                }}
                className='response-bubble'
              >
                {' '}
                A{' '}
              </div>
              <div
                style={{
                  backgroundColor:
                    question.answer == 'B' ? '#a5f390' : 'transparent',
                }}
                className='response-bubble'
              >
                {' '}
                B{' '}
              </div>
              <div
                style={{
                  backgroundColor:
                    question.answer == 'C' ? '#a5f390' : 'transparent',
                }}
                className='response-bubble'
              >
                {' '}
                C{' '}
              </div>
              <div
                style={{
                  backgroundColor:
                    question.answer == 'D' ? '#a5f390' : 'transparent',
                }}
                className='response-bubble'
              >
                {' '}
                D{' '}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Template;
