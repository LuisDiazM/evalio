import './App.css';
import ListGroup from './components/groups/listGroup/ListGroup';
import Group from './components/groups/viewGroup/Group';

import { createBrowserRouter, RouterProvider } from 'react-router';
import TemplateView from './components/templates/templateview/Template';
import TemplateForm from './components/templates/templateForm/TemplateForm';
import QualificationView from './components/qualifications/qualification/Qualification';
import UploadEvaluation from './components/evaluations/uploadeval/UploadEvaluation';
import ListEvaluations from './components/evaluations/listEvaluations/ListEvaluations';
import Login from './components/Login';
import Signup from './components/Signup';
import PrivateRoute from './components/PrivateRoute';

const router = createBrowserRouter([
  { path: '/', element: <Login />, index: true },
  { path: '/login', element: <Login /> },
  { path: '/signup', element: <Signup /> },
  
  { path: '/groups', element: <PrivateRoute><ListGroup /></PrivateRoute> },
  { path: '/group/:id', element: <PrivateRoute><Group /></PrivateRoute> },
  { path: '/template/group/:groupId', element: <PrivateRoute><TemplateForm /></PrivateRoute> },
  { path: '/template/:id', element: <PrivateRoute><TemplateView /></PrivateRoute> },
  { path: '/qualification/template/:id', element: <PrivateRoute><QualificationView /></PrivateRoute> },
  { path: '/evaluation', element: <PrivateRoute><UploadEvaluation /></PrivateRoute> },
  { path: '/evaluations/group/:groupId/template/:templateId', element: <PrivateRoute><ListEvaluations /></PrivateRoute> },
]);

function App() {
  return (
    <>
      <main>
        <RouterProvider router={router} />
      </main>
    </>
  );
}

export default App;
