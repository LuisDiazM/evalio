import { useNavigate, useParams } from 'react-router';
import Navbar from '../../navbar/navbar';
import './templateForm.css';
import { useRef, useState } from 'react';

const TemplateForm = () => {
  const { groupId } = useParams<{ groupId: string }>();
  console.log(groupId);
  const navigate = useNavigate();

  const answerOptions = ['A', 'B', 'C', 'D'];
  const subjectForm = useRef<HTMLInputElement>(null);
  const periodForm = useRef<HTMLInputElement>(null);
  const testNumberForm = useRef<HTMLSelectElement>(null);
  const [questionNumber, setQuestionNumber] = useState<number>(0);
  const defaultQuestions = [...Array(questionNumber).keys()];

  const [studentResponses, setStudentResponses] = useState<{
    [questionId: number]: string;
  }>({});
  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();

    const testNumber = testNumberForm.current?.value;
    const subject = subjectForm.current?.value;
    const period = subjectForm.current?.value;

    if (testNumber && subject && period && questionNumber > 0) {
      navigate(`/templates/group/${groupId}`);
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

  return (
    <>
      <Navbar />
      <div className='container-template'>
        <form onSubmit={handleSubmit} className='template-card'>
          <label>
            Materia
            <input ref={subjectForm} name='subject' key={0} type='text'></input>
          </label>
          <label>
            Periodo
            <input ref={periodForm} key={1} name='period'></input>
          </label>
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
