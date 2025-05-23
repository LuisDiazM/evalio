import './App.css';
import ListGroup from './components/groups/listGroup/ListGroup';
import Group from './components/groups/viewGroup/Group';

import { createBrowserRouter, RouterProvider } from 'react-router';
import TemplateView from './components/templates/templateview/Template';
import TemplateForm from './components/templates/templateForm/TemplateForm';
import QualificationView from './components/qualifications/qualification/Qualification';
import UploadEvaluation from './components/evaluations/uploadeval/UploadEvaluation';
import ListEvaluations from './components/evaluations/listEvaluations/ListEvaluations';
const router = createBrowserRouter([
  { path: '/', element: <ListGroup></ListGroup>, index: true },
  {
    path: '/groups',
    element: <ListGroup></ListGroup>,
  },
  { path: '/group/:id', element: <Group></Group> },
  { path: '/template/group/:groupId', element: <TemplateForm></TemplateForm> },
  { path: '/template/:id', element: <TemplateView></TemplateView> },
  {
    path: '/qualification/template/:id',
    element: <QualificationView></QualificationView>,
  },
  { path: '/evaluation', element: <UploadEvaluation></UploadEvaluation> },
  { path: '/evaluations/group/:groupId/template/:templateId', element: <ListEvaluations></ListEvaluations> },
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
