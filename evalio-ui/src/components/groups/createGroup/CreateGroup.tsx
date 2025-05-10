import { useState, type FormEvent } from 'react';
import './createGroup.css';

interface FormFieldsGroup {
  groupName: string;
  period: string;
  subjectName: string;
  file: File | null;
}
const CreateGroup = () => {
  const [errorForm, setErrorForm] = useState<string>('');

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const fields = Object.fromEntries(
      new window.FormData(event.target as HTMLFormElement)
    ) as unknown as FormFieldsGroup;
    const { groupName, period, subjectName, file } = fields;
    if (groupName == '' || period == '' || subjectName == '' || file == null) {
      setErrorForm('El formulario no puede tener ningún campo vacío');
    } else {
      setErrorForm('');
    }
    if (file?.type != 'text/csv') {
      setErrorForm(`el archivo ${file?.name} debe ser csv`);
    }
  };

  return (
    <>
      <form
        onSubmit={handleSubmit}
        style={{ borderColor: errorForm != '' ? 'red' : '' }}
      >
        <label>
          Nombre del grupo
          <input key={0} name='groupName' type='text' placeholder='E01'></input>
        </label>
        <label>
          Periodo académico
          <input key={1} name='period' type='text' placeholder='2025-1'></input>
        </label>
        <label>
          Nombre de la materia
          <input
            id='subjectInput'
            key={2}
            name='subjectName'
            type='text'
            placeholder='Gestiones administrativas'
          ></input>
        </label>
        <label>
          Listado de estudiantes CSV, por ejemplo:
          <span className='tooltip-trigger'></span>
          <table>
            <thead>
              <tr>
                <th>Documento</th>
                <th>Nombre</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>1000000</td>
                <td>CARLOS DIAZ</td>
              </tr>
              <tr>
                <td>2000000</td>
                <td>MELISSA GALINDO</td>
              </tr>
            </tbody>
          </table>
          <input type='file' name='file' />
        </label>
        <button type='submit'>Crear grupo</button>
      </form>
      {errorForm != '' && <p>{errorForm}</p>}
    </>
  );
};

export default CreateGroup;
