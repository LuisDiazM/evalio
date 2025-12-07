import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

import en from '@/i18n/locales/en/translation.json';
import es from '@/i18n/locales/es/translation.json';

i18n
  .use(initReactI18next)
  .init({
    resources: {
      en: { translation: en },
      es: { translation: es },
    },
    lng: 'es',
    fallbackLng: 'en',
    interpolation: { escapeValue: false },
  });

export default i18n;
