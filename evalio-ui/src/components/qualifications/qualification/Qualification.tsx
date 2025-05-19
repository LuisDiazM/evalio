import { useEffect, useState } from 'react';
import Navbar from '../../navbar/navbar';
import './qualification.css';
import { useParams } from 'react-router';
import { getSummaryByTemplateId } from '../../../services/manager/managerService';
import type { Qualification } from '../../../services/manager/entities/qualifications';
const QualificationView = () => {
  const { id } = useParams<{ id: string }>();
  const [qualification, setQualification] = useState<Qualification | null>(
    null
  );
  useEffect(() => {
    if (id) {
      getSummaryByTemplateId(id).then((data) => {
        setQualification(data);
      });
    }

    return () => {};
  }, [id]);

  return (
    <>
      <Navbar></Navbar>
      <div className='qualification-container'>
        <button>Exportar</button>
        <h5>
          {' '}
          Corte # <strong> {qualification?.number} </strong>{' '}
        </h5>
        <h5>
          Periodo <strong>{qualification?.period}</strong>{' '}
        </h5>
        <table>
          <th>Identificación</th>
          <th>Estudiante</th>
          <th>Calificación</th>
          <th>Ver</th>
          {qualification?.students.map((student) => {
            return (
              <tr key={student.student_identification}>
                <td> {student.student_identification}</td>
                <td>{student.student_name}</td>
                <td>{student.score}</td>
                <td>Ver</td>
              </tr>
            );
          })}
        </table>
      </div>
    </>
  );
};

export default QualificationView;
