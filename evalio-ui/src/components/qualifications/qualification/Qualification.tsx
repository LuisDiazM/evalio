import { useEffect, useState } from 'react';
import Navbar from '../../navbar/navbar';
import './qualification.css';
import { Link, useParams } from 'react-router';
import {
  generateCsvSummaryQualifications,
  getSummaryByTemplateId,
} from '../../../services/manager/managerService';
import type { Qualification } from '../../../services/manager/entities/qualifications';
import uploadIcon from '../../../assets/icons8-upload-50.png';
const QualificationView = () => {
  const { id } = useParams<{ id: string }>();
  const [qualification, setQualification] = useState<Qualification | null>(
    null
  );
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  useEffect(() => {
    if (id) {
      getSummaryByTemplateId(id).then((data) => {
        setQualification(data);
      });
    }

    return () => { };
  }, [id]);


  const handleExportQualifications = (templateId: string | undefined) => {
    if (templateId) {
      generateCsvSummaryQualifications(templateId).then();
    }
  };

  const handleViewExam = (examPath: string) => {
    setSelectedImage(examPath);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedImage(null);
  };

  return (
    <>
      <Navbar></Navbar>
      {qualification && (
        <div className='qualification-container'>
          <button onClick={() => handleExportQualifications(id)}>
            Exportar
          </button>
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
                  <button
                    className="view-exam-btn"
                    onClick={() => handleViewExam(student.exam_path)}
                    title="Ver examen"
                  >
                    👁️
                  </button>
                </tr>
              );
            })}
          </table>
        </div>
      )}
      {!qualification && (
        <div className='no-data'>
          <h1>No tenemos calificaciones reportadas</h1>
          <h5>Para que se generen calificaciones debes subir los parciales</h5>
          <Link to={'/evaluation'}>
            <img src={uploadIcon} alt='subir'></img>
          </Link>
        </div>
      )}
      {isModalOpen && selectedImage && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={closeModal}>
              ✕
            </button>
            <img
              src={selectedImage}
              alt="Examen del estudiante"
              className="exam-image"
            />
          </div>
        </div>
      )}
    </>
  );
};

export default QualificationView;
