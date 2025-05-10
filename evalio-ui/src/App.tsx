import './App.css';
import ListGroup from './components/groups/listGroup/ListGroup';
import Group from './components/groups/listGroup/viewGroup/Group';
import Navbar from './components/navbar/navbar';

import { createBrowserRouter, RouterProvider } from 'react-router';
import ListTemplates from './components/templates/listTemplates/ListTemplates';
import Template from './components/templates/templateview/Template';
const router = createBrowserRouter([
  {
    path: '/groups',
    element: <ListGroup></ListGroup>,
  },
  { path: '/group/:id', element: <Group></Group> },
  { path: '/templates', element: <ListTemplates></ListTemplates> },
  { path: '/template/:id', element: <Template></Template> },
]);
function App() {
  return (
    <>
      <main>
        <Navbar></Navbar>
        <RouterProvider router={router} />
      </main>
    </>
  );
}

export default App;
