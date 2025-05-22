import { useEffect, useState } from 'react';
import Navbar from '../../navbar/navbar';
import './template.css';

import { useNavigate, useParams } from 'react-router';
import {
  getTemplateById,
  getTemplateSheet,
} from '../../../services/manager/managerService';
import type { Template } from '../../../services/manager/entities/templates';

const TemplateView = () => {
  // const template = templates[0];
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const [template, setTemplate] = useState<Template | null>(null);
  useEffect(() => {
    if (id) {
      getTemplateById(id).then((data) => {
        setTemplate(data);
      });
    }
    return () => {};
  }, [id]);

  const handleQualifications = (id: string | undefined) => {
    if (id) {
      navigate(`/qualification/template/${id}`);
    }
  };

  const handleGenerateTemplateSheets = (
    groupId: string | undefined,
    templateId: string | undefined
  ) => {
    if (groupId && templateId) {
      getTemplateSheet(groupId, templateId).then();
    }
  };

  return (
    <>
      <Navbar></Navbar>
      <div className='container-template'>
        <div>
          <h5>Hojas de respuestas para estudiantes</h5>
          <button
            onClick={() =>
              handleGenerateTemplateSheets(template?.group_id, template?.id)
            }
          >
            Generar
          </button>
        </div>

        <div className='template-card'>
          <button onClick={() => handleQualifications(id)}>
            Ver calificaciones
          </button>
          <div key={template?.id}>
            <h5>
              {' '}
              Materia <strong>{template?.subject_name} </strong>{' '}
            </h5>
            <h5>
              {' '}
              Periodo <strong>{template?.period}</strong>
            </h5>
            <h5>
              {' '}
              Corte <strong># {template?.number}</strong>
            </h5>
            <h5>
              {' '}
              Cantidad de preguntas{' '}
              <strong>{template?.questions.length}</strong>
            </h5>
          </div>
          <div className='questions-list'>
            {template?.questions.map((question, index) => {
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
      </div>
    </>
  );
};

export default TemplateView;
