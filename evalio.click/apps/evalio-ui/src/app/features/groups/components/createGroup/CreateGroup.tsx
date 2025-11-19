import React, { useState } from 'react';
import { useFormik } from 'formik';
import {
  CreateGroupForm,
  CreateGroupSchema,
} from '@/features/groups/models/createGroup.form';
import styles from './createGroup.module.scss';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { createGroup } from '@/features/groups/services/groups.service';

type StudentRow = { documento: string; nombre: string };

const CreateGroup: React.FC = () => {
  const [preview, ] = useState<StudentRow[]>([
    { documento: '1000000', nombre: 'CARLOS DIAZ' },
    { documento: '2000000', nombre: 'MELISSA GALINDO' }
  ]);
  const navigate = useNavigate();

  const handleBack = () => {
    navigate('/groups');
  };

  const formik = useFormik<CreateGroupForm>({
    initialValues: {
      file: null,
      groupName: '',
      period: '',
      subjectName: '',
    },
    validationSchema: CreateGroupSchema,
    onSubmit: async (values) => {
      // map formik values to payload
      mutation.mutate({
        file: values.file,
        name: values.groupName,
        subject_name: values.subjectName,
        period: values.period,
      });
    },
  });

  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: (payload: { file: File | null; name: string; subject_name: string; period: string }) =>
      createGroup(payload),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['groups'] });
      navigate('/groups');
    },
    onError: (err: unknown) => {
      const message = err instanceof Error ? err.message : String(err);
      console.error('createGroup error', message);
      // could set an error state or rely on mutation.error
    },
  });

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.currentTarget.files && e.currentTarget.files[0];
    formik.setFieldValue('file', f || null);
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <button type="button" aria-label="Volver a grupos" className={styles.backBtn} onClick={handleBack}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">
            <polyline points="15 18 9 12 15 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </button>
        <h2 className={styles.title}>Crear Nuevo Grupo</h2>
      </div>
      <form onSubmit={formik.handleSubmit} className={styles.form}>
        <div className={styles.field}>
          <label className={styles.label}>Nombre del grupo</label>
          <input
            className={styles.input}
            name="groupName"
            value={formik.values.groupName}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
          />
          {formik.touched.groupName && formik.errors.groupName && (
            <div className={styles.error}>{formik.errors.groupName}</div>
          )}
        </div>

        <div className={styles.field}>
          <label className={styles.label}>Periodo académico</label>
          <input
            className={styles.input}
            name="period"
            value={formik.values.period}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
          />
          {formik.touched.period && formik.errors.period && (
            <div className={styles.error}>{formik.errors.period}</div>
          )}
        </div>

        <div className={styles.field}>
          <label className={styles.label}>Nombre de la materia</label>
          <input
            className={styles.input}
            name="subjectName"
            value={formik.values.subjectName}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
          />
          {formik.touched.subjectName && formik.errors.subjectName && (
            <div className={styles.error}>{formik.errors.subjectName}</div>
          )}
        </div>

        <div className={styles.field}>
          <label className={styles.label}>
            Listado de estudiantes CSV, por ejemplo:
          </label>

          <div className={styles.tableWrapper}>
            <table className={styles.table}>
              <thead>
                <tr>
                  <th>DOCUMENTO</th>
                  <th>NOMBRE</th>
                </tr>
              </thead>
              <tbody>
                {preview.length === 0 && (
                  <tr>
                    <td colSpan={2} className={styles.help}>
                      Sin filas de ejemplo
                    </td>
                  </tr>
                )}
                {preview.map((r, i) => (
                  <tr key={i}>
                    <td>{r.documento}</td>
                    <td>{r.nombre}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className={styles.dashedBox}>
            <label className={styles.fileLabel}>
              <input
                className={styles.fileInput}
                type="file"
                accept=".csv,text/csv"
                onChange={handleFileChange}
              />
              <div className={styles.help}>Seleccionar archivo</div>
            </label>
            <div className={styles.fileName}>
              {formik.values.file
                ? formik.values.file.name
                : 'Sin archivos seleccionados'}
            </div>
            {formik.touched.file && formik.errors.file && (
              <div className={styles.error}>{String(formik.errors.file)}</div>
            )}
          </div>
        </div>

        <div>
          <button type="submit" className={styles.submitBtn} disabled={mutation.status === 'pending'}>
            {mutation.status === 'pending' ? 'Creando...' : 'Crear grupo'}
          </button>
          {mutation.status === 'error' && (
            <div className={styles.error} style={{ marginTop: 8 }}>
              {(mutation.error as Error)?.message || 'Error al crear grupo'}
            </div>
          )}
        </div>
      </form>
    </div>
  );
};

export default CreateGroup;
