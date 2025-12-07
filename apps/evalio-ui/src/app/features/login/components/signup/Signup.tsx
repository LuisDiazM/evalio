import { useFormik } from 'formik';
import styles from './signup.module.scss';
import { useTranslation } from 'react-i18next';
import { SignupForm, SignupSchema } from '@/features/login/models/signup.form';
import { signup } from '@/features/login/services';
import { useNavigate } from 'react-router-dom';

const initialValues: SignupForm = {
  fullName: '',
  email: '',
  password: '',
  confirmPassword: '',
};

const Signup = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();

  const submitSignupForm = async (values: SignupForm) => {
    try {
      const isValid = formik.isValid;
      if (isValid) {
        const status = await signup(values.email, values.password, values.fullName);
        if(status === 201){
          // signup endpoint currently returns status only; if it returned a token, we would set user here
          // Example: setUserFromToken(response.token)
          navigate('/groups')
        }
      }
    } catch (err) {
      console.error('[submitSignupForm] error:', err);
    }
  };
  // signup currently doesn't return a token; no-op for now
  const formik = useFormik({
    initialValues: initialValues,
    onSubmit: submitSignupForm,
    validationSchema: SignupSchema,
  });

  return (
    <div className={styles['signup-wrapper']}>
      <form onSubmit={formik.handleSubmit} className={styles['signup-form']}>
        <div className={styles.field}>
          <label htmlFor="fullName" className={styles.label}>
            {t('signup.fullName', 'Nombre completo')}
          </label>
          <input
            type="text"
            id="fullName"
            placeholder={t('signup.fullName', 'Jhon Doe')}
            required
            className={styles.input}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.fullName}
          />
        </div>
        <div className={styles.field}>
          <label className={styles.label} htmlFor="email">
            {t('signup.email', 'Correo electrónico')}
          </label>
          <input
            type="email"
            id="email"
            placeholder={t('signup.email', 'myemail@example.com')}
            required
            className={styles.input}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.email}
          />
          {formik.touched.email && formik.errors.email ? (
            <div className={styles.error}>{String(formik.errors.email)}</div>
          ) : null}
        </div>
        <div className={styles.field}>
          <label className={styles.label} htmlFor="password">
            {t('signup.password', 'Contraseña')}
          </label>
          <input
            type="password"
            id="password"
            placeholder={t('signup.password', 'mysecretpassword')}
            required
            className={styles.input}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.password}
          />
        </div>

        <div className={styles.field}>
          <label className={styles.label} htmlFor="confirmPassword">
            {t('signup.confirmPassword', 'Confirmar contraseña')}
          </label>
          <input
            type="password"
            id="confirmPassword"
            placeholder={t('signup.confirmPassword', 'Contraseña')}
            required
            className={styles.input}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.confirmPassword}
          />
        </div>

        {formik.touched.confirmPassword && formik.errors.confirmPassword ? (
          <div className={styles.error}>{t(formik.errors.confirmPassword)}</div>
        ) : null}

        {formik.touched.password && formik.errors.password ? (
          <div className={styles.error}>{t(formik.errors.password)}</div>
        ) : null}

        <div className={styles.actions}>
          <button type="submit" className={styles.submit}>
            {t('signup.submit', 'Crear cuenta')}
          </button>
          <div>
            <a href="/login" className={styles.link}>
              {t('signup.alreadyHaveAccount', 'Ya tiene una cuenta? Ingresar')}
            </a>
          </div>
        </div>
      </form>
    </div>
  );
};

export default Signup;
