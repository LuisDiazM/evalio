import * as Yup from 'yup';

export interface LoginForm {
  email: string;
  password: string;
}

export const LoginSchema = Yup.object().shape({
  email: Yup.string().email('login.invalidEmail').required('login.emailRequired'),
  password: Yup.string()
    .min(6, 'login.invalidPassword')
    .required('login.passwordRequired'),
});
