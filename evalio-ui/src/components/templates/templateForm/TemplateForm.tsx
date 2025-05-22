import { useNavigate, useParams } from 'react-router';
import Navbar from '../../navbar/navbar';
import './templateForm.css';
import { useEffect, useRef, useState } from 'react';
import type { CreateTemplate } from '../../../services/manager/entities/templates';
import {
  createTemplate,
  getGroupById,
} from '../../../services/manager/managerService';
import type { Groups } from '../../../services/manager/entities/groups';

const TemplateForm = () => {
  const { groupId } = useParams<{ groupId: string }>();
  const navigate = useNavigate();

  const answerOptions = ['A', 'B', 'C', 'D'];
  const testNumberForm = useRef<HTMLSelectElement>(null);
  const [questionNumber, setQuestionNumber] = useState<number>(0);
  const defaultQuestions = [...Array(questionNumber).keys()];
  const [group, setGroup] = useState<Groups | null>(null);
  const [studentResponses, setStudentResponses] = useState<{
    [questionId: number]: string;
  }>({});
  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();

    const testNumber = testNumberForm.current?.value;

    if (groupId && testNumber && questionNumber > 0) {
      const questions = Object.entries(studentResponses).map(
        ([key, value]) => ({
          question: Number(key),
          answer: value,
        })
      );
      const templateData: CreateTemplate = {
        group_id: groupId,
        number: parseInt(testNumber, 10),
        period: group?.period ? group.period : '',
        subject_name: group?.subject_name ? group.subject_name : '',
        questions,
      };
      createTemplate(templateData).then((data) => {
        if (data != null) {
          navigate(`/group/${groupId}/templates`);
        }
      });
    }
  };

  const handleResponseChange = (question: number, response: string) => {
    setStudentResponses({ ...studentResponses, [question]: response });
  };

  const handleQuestionNumber = (event: React.ChangeEvent<HTMLInputElement>) => {
    const questions = Number(event.target.value);
    if (questions >= 15) {
      return;
    }
    setQuestionNumber(questions);
  };

  useEffect(() => {
    if (groupId) {
      getGroupById(groupId).then((data) => {
        setGroup(data);
      });
    }
    return () => {};
  }, [groupId]);

  return (
    <>
      <Navbar />
      <div className='container-template'>
        <form onSubmit={handleSubmit} className='template-card'>
          <label>
            Corte
            <select ref={testNumberForm} name='number'>
              <option> 1 </option>
              <option> 2 </option>
              <option> 3 </option>
            </select>
          </label>
          <label>
            # Preguntas
            <input
              type='number'
              onChange={(event) => handleQuestionNumber(event)}
              max={15}
              min={0}
            ></input>
          </label>
          {questionNumber > 0 && (
            <div className='questions-list'>
              <div className='questions-responses'>
                <h5>A</h5>
                <h5>B</h5>
                <h5>C</h5>
                <h5>D</h5>
              </div>

              {defaultQuestions.map((questionIndex) => (
                <div key={questionIndex}>
                  <label className='response-bubble'>
                    {questionIndex + 1}
                    {answerOptions.map((option) => (
                      <input
                        type='radio'
                        name={`question-${questionIndex + 1}`}
                        value={option}
                        checked={studentResponses[questionIndex + 1] === option}
                        onChange={() =>
                          handleResponseChange(questionIndex + 1, option)
                        }
                        key={`${questionIndex + 1}-${option}`}
                      ></input>
                    ))}
                  </label>
                </div>
              ))}
            </div>
          )}
          {questionNumber > 0 && <button> Guardar</button>}
        </form>
      </div>
    </>
  );
};

export default TemplateForm;
