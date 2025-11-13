import styles from './login.module.scss';
import { useTranslation } from 'react-i18next';
import { useFormik } from 'formik';
import { LoginForm, LoginSchema } from '@/features/login/models/login.form';
import { login } from '../../services';

const initialValues: LoginForm = {
  email: '',
  password: '',
};

const Login = () => {
  const { t } = useTranslation();

  const submitLoginForm = async (values: LoginForm) => {
    const isValid = LoginSchema.isValidSync(values);
    if (isValid) {
      const response = await login(values.email, values.password);
      if (response?.token) {
        localStorage.setItem('access_token', response.token);
      }
    }
  };

  const formik = useFormik({
    initialValues: initialValues,
    onSubmit: submitLoginForm,
    validationSchema: LoginSchema,
  });

  return (
    <form onSubmit={formik.handleSubmit} className={styles.form}>
      <h2 className={styles.title}>{t('login.title')}</h2>

      <label htmlFor="email" className={styles.label}>
        {t('login.email')}
      </label>
      <input
        id="email"
        name="email"
        type="email"
        placeholder={t('login.email')}
        required
        className={styles.input}
        onChange={formik.handleChange}
        onBlur={formik.handleBlur}
        value={formik.values.email}
      />
      {formik.touched.email && formik.errors.email ? (
        <div className={styles.error}>{t(formik.errors.email)}</div>
      ) : null}
      <label htmlFor="password" className={styles.label}>
        {t('login.password')}
      </label>
      <input
        id="password"
        name="password"
        type="password"
        placeholder={t('login.password')}
        required
        className={styles.input}
        onChange={formik.handleChange}
        onBlur={formik.handleBlur}
        value={formik.values.password}
      />
      {formik.touched.password && formik.errors.password ? (
        <div className={styles.error}>{t(formik.errors.password)}</div>
      ) : null}
      <button type="submit" className={styles.submit}>
        {t('login.submit')}
      </button>

      <a href="/signup" className={styles.signup}>
        {t('login.noAccount')}
      </a>
    </form>
  );
};

export default Login;
