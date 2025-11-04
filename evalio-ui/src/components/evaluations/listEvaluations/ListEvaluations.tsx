import { useParams } from 'react-router';
import Navbar from '../../navbar/navbar';
// import evaluations from '../../mocks/evaluations.json';
import './listEvaluations.css';
import { useEffect, useState } from 'react';
import {
  getExamsByTemplate,
  getGroupById,
} from '../../../services/manager/managerService';
import type { Groups } from '../../../services/manager/entities/groups';
import type { ExamResponse } from '../../../services/manager/entities/exams';
const ListEvaluations = () => {
  const { groupId, templateId } = useParams<{
    groupId: string;
    templateId: string;
  }>();

  const [group, setGroup] = useState<Groups | null>(null);
  const [evaluations, setEvaluations] = useState<ExamResponse[]>([]);

  useEffect(() => {
    console.log(groupId, templateId);
    if (groupId && templateId) {
      getGroupById(groupId).then((group) => {
        if (group != null) {
          setGroup(group);
          getExamsByTemplate(templateId).then((exams) => {
            setEvaluations([...exams]);
          });
        }
      });
    }
    return () => {};
  }, [groupId, templateId]);

  return (
    <>
      <Navbar />
      {group && (
        <div className='container-list-evaluations'>
          <h5>
            En la tabla puede ver los estudiantes y los estados de calificación
          </h5>
          <table>
            <thead>
              <tr>
                <th>Identificación</th>
                <th>Nombre</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              {group?.students.map((student) => {
                const evaluation = evaluations.find(
                  (ev) => ev.student_identification === student.identification
                );
                const estadoMap: Record<
                  string,
                  { label: string; color: string }
                > = {
                  pending_upload: {
                    label: 'Pendiente por subir',
                    color: '#fffab7',
                  },
                  error: { label: 'Error', color: 'red' },
                  completed: { label: 'Completado', color: '#4589ee' },
                  pending: { label: 'Procesando', color: '#a2e278' },
                };

                const statusKey = evaluation?.status || 'pending_upload';
                const estadoInfo =
                  estadoMap[statusKey] || estadoMap['pending_upload'];

                return (
                  <tr key={student.identification}>
                    <td>{student.identification}</td>
                    <td>{student.name}</td>
                    <td>
                      <span
                        style={{
                          backgroundColor: estadoInfo.color,
                          padding: '4px 8px',
                          borderRadius: '4px',
                          fontWeight: 500,
                        }}
                      >
                        {estadoInfo.label}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
};

export default ListEvaluations;
