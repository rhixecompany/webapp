import { HashRouter as Router, Route, Switch } from "react-router-dom";
import Navigation from "./components/layout/Navigation";
import Footer from "./components/layout/Footer";
import "./App.css";
import Dashboard from "./pages/Free/Dashboard";
import Home from "./pages/Free/Home";
import Login from "./pages/Free/Login";
import Register from "./pages/Free/Register";
import Comic from "./pages/Free/Comic";
import Chapter from "./pages/Free/Chapter";
import Users from "./pages/Protected/Users";
import UsersEdit from "./pages/Protected/UsersEdit";
import Profile from "./pages/Protected/Profile";
import Comics from "./pages/Protected/Comics";
import Chapters from "./pages/Protected/Chapters";
import Bookmarks from "./pages/Protected/Bookmarks";
import ComicCreate from "./pages/Protected/ComicCreate";
import ComicEdit from "./pages/Protected/ComicEdit";
import ChapterCreate from "./pages/Protected/ChapterCreate";
import ChapterEdit from "./pages/Protected/ChapterEdit";
import Scraper from "./pages/Protected/Scraper";
import Genre from "./pages/Free/Genre";
import Cat from "./pages/Free/Cat";
import Search from "./pages/Free/Search";
function App() {
  return (
    <Router>
      <div className="App">
        <Navigation />
        <main className="py-3">
          <Switch>
            <Route path="/" component={Dashboard} exact />
            <Route path="/blog" component={Home} />
            <Route path="/login" component={Login} />
            <Route path="/register" component={Register} />
            <Route path="/profile" component={Profile} />
            <Route path="/admin/users" component={Users} />
            <Route path="/admin/user/:id/edit" component={UsersEdit} />
            <Route path="/comic/:id" component={Comic} />
            <Route path="/chapter/:id" component={Chapter} />
            <Route path="/admin/comic/:id/edit" component={ComicEdit} />
            <Route path="/admin/comic/create" component={ComicCreate} />
            <Route path="/admin/chapter/:id/edit" component={ChapterEdit} />
            <Route path="/admin/chapter/create" component={ChapterCreate} />
            <Route path="/comic/:id" component={Comic} />
            <Route path="/chapter/:id" component={Chapter} />
            <Route path="/admin/chapterslist" component={Chapters} />
            <Route path="/admin/comicslist" component={Comics} />
            <Route path="/bookmarks" component={Bookmarks} />
            <Route path="/admin/scraper" component={Scraper} />
            <Route path="/genre/:id" component={Genre} />
            <Route path="/category/:id" component={Cat} />
            <Route path="/search" component={Search} />
          </Switch>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
