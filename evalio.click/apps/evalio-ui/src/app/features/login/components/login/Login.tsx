import styles from './login.module.scss';

const Login = () => {
  return (
      <div className={styles.container}>
      <form className={styles.form}>
        <h2 className={styles.title}>Ingrese a su cuenta</h2>

        <div className={styles.field}>
          <label htmlFor="email" className={styles.label}>Email</label>
          <input
            id="email"
            type="email"
            placeholder="myemail@example.com"
            required
            className={styles.input}
          />
        </div>

        <div className={styles.fieldSmall}>
          <label htmlFor="password" className={styles.label}>Contraseña</label>
          <input
            id="password"
            type="password"
            placeholder="Enter your password"
            required
            className={styles.input}
          />
        </div>


        <button type="submit" className={styles.submit}>Ingresar</button>

        <div className={styles.right}>
          <a href="/signup" className={styles.signup}>No tiene una cuenta? Registrarse</a>
        </div>
      </form>
    </div>
  )
}

export default Login
