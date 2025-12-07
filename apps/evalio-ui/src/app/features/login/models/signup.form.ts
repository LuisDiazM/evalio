import * as Yup from 'yup';

export interface SignupForm {
  fullName: string;
  email: string;
  password: string;
  confirmPassword: string;
}

export const SignupSchema = Yup.object().shape({
  fullName: Yup.string().required('signup.fullNameRequired'),
  email: Yup.string()
    .email('signup.invalidEmail')
    .required('signup.emailRequired'),
  password: Yup.string()
    .min(6, 'signup.invalidPassword')
    .required('signup.passwordRequired'),
  confirmPassword: Yup.string()
    .oneOf([Yup.ref('password'), ''], 'signup.passwordsMustMatch')
    .required('signup.confirmPasswordRequired'),
});
