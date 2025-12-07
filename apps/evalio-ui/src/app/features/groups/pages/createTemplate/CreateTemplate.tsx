import React from 'react';
import { useFormik } from 'formik';
import CreateTemplateSchema, { CreateTemplateForm } from '@/features/groups/models/createTemplate.form';
import styles from './createTemplate.module.scss';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { createTemplate, CreateTemplatePayload } from '@/features/groups/services/groups.service';
import { useNavigate } from 'react-router-dom';

type Props = {
  group_id?: string;
  period?: string;
  subject_name?: string;
  onCreated?: (data?: any) => void;
  onCancel?: () => void;
};

const CreateTemplate: React.FC<Props> = ({ group_id = '', period = '', subject_name = '', onCreated, onCancel }) => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const formik = useFormik<CreateTemplateForm>({
    initialValues: {
      group_id,
      number: 1,
      period,
      subject_name,
      questionsCount: 4,
      questions: Array.from({ length: 4 }).map((_, i) => ({ question: i + 1, answer: '' })),
    },
    validationSchema: CreateTemplateSchema,
    onSubmit: (values) => {
      const payload: CreateTemplatePayload = {
        group_id: values.group_id,
        number: values.number,
        period: values.period,
        subject_name: values.subject_name,
        questions: values.questions,
      };

      mutation.mutate(payload);
    },
  });

  const mutation = useMutation({
    mutationFn: (payload: CreateTemplatePayload) => createTemplate(payload),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['templates'] });
      if (onCreated) {
        onCreated(data);
      } else {
        navigate(-1);
      }
    },
  });

  const handleQuestionsCountChange = (n: number) => {
    const count = Math.max(1, n);
    formik.setFieldValue('questionsCount', count);
    formik.setFieldValue('questions', Array.from({ length: count }).map((_, i) => ({ question: i + 1, answer: '' })));
  };

  const setAnswer = (index: number, answer: string) => {
    const q = [...formik.values.questions];
    q[index] = { ...q[index], answer };
    formik.setFieldValue('questions', q);
  };

  return (
    <div className={styles.container}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <h2>Crear Plantilla</h2>
        {onCancel && (
          <button type="button" onClick={onCancel} className={styles.cancelBtn}>
            Cancelar
          </button>
        )}
      </div>
      <form onSubmit={formik.handleSubmit} className={styles.form}>
        <div className={styles.field}>
          <label>Group Id</label>
          <input disabled {...formik.getFieldProps('group_id')} />
        </div>

        <div className={styles.field}>
          <label>Periodo</label>
          <input disabled {...formik.getFieldProps('period')} />
        </div>

        <div className={styles.field}>
          <label>Numero (parcial) - max 5</label>
          <input
            type="number"
            name="number"
            min={1}
            max={5}
            value={formik.values.number}
            onChange={(e) => formik.setFieldValue('number', Number(e.target.value))}
          />
        </div>

        <div className={styles.field}>
          <label>Materia</label>
          <input disabled {...formik.getFieldProps('subject_name')} />
        </div>

        <div className={styles.field}>
          <label>Cantidad de preguntas</label>
          <input
            type="number"
            min={1}
            max={15}
            value={formik.values.questionsCount}
            onChange={(e) => handleQuestionsCountChange(Number(e.target.value))}
          />
        </div>

        <div className={styles.sheet}>
          {formik.values.questions.map((q: { question: number; answer: string }, i: number) => (
            <div key={i} className={styles.questionRow}>
              <div className={styles.index}>{q.question}.</div>
              <div className={styles.options}>
                {['A', 'B', 'C', 'D'].map((opt) => (
                  <label key={opt} className={styles.optionLabel}>
                    <input
                      type="radio"
                      name={`question-${i}`}
                      value={opt}
                      checked={formik.values.questions[i]?.answer === opt}
                      onChange={() => setAnswer(i, opt)}
                    />
                    {opt}
                  </label>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className={styles.actions}>
          <button type="submit" disabled={mutation.status === 'pending'}>
            {mutation.status === 'pending' ? 'Creando...' : 'Crear plantilla'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default CreateTemplate;
