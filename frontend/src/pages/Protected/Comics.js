import React, { useEffect, Fragment } from "react";
import Loader from "../../components/features/Loader";
import Message from "../../components/features/Message";
import Paginate from "../../components/features/Paginate";
import { useDispatch, useSelector } from "react-redux";
import { listComics, deleteComic } from "../../actions/comicsActions";
import { Table, Button, Container, Image, Row, Col } from "react-bootstrap";
import { FaEdit, FaTrash, FaPlus } from "react-icons/fa";
import { Link } from "react-router-dom";
import { LinkContainer } from "react-router-bootstrap";
const Comics = ({ history }) => {
  let keyword = history.location.search;
  const dispatch = useDispatch();
  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;
  const comicsList = useSelector((state) => state.comicsList);
  const { comics, error, loading, pages, page, count } = comicsList;
  const comicDelete = useSelector((state) => state.comicDelete);
  const {
    loading: loadingDelete,
    error: errorDelete,
    success: successDelete,
  } = comicDelete;
  useEffect(() => {
    if (!userInfo || !userInfo.isAdmin) {
      history.push("/login");
    }
    dispatch(listComics(keyword));
  }, [dispatch, history, keyword, successDelete, userInfo]);

  const deleteHandler = (title) => {
    if (window.confirm(`Are you sure you want to delete:${title}`)) {
      dispatch(deleteComic(title));
    }
  };

  return (
    <Fragment>
      {loadingDelete && <Loader />}
      {errorDelete && <Message variant="danger">{errorDelete}</Message>}
      {loading ? (
        <Loader />
      ) : error ? (
        <Message variant="danger">{error}</Message>
      ) : (
        <Container>
          <Row className="align-items-center">
            <Col>
              <h2>Total Comics: {count}</h2>
            </Col>
            <Col className="text-right">
              <Button variant="secondary">
                <Link to={"/admin/comic/create"}>
                  <FaPlus /> Create New Comic
                </Link>
              </Button>
            </Col>
          </Row>

          <Row>
            <Col>
              <Table
                className="table table-sm text-white"
                striped
                bordered
                hover
                responsive
              >
                <thead>
                  <tr>
                    <th>Title</th>
                    <th>Image</th>

                    <th></th>
                    <th></th>
                  </tr>
                </thead>

                <tbody>
                  {comics?.map((comic) => (
                    <tr key={comic._id}>
                      <td>
                        <Link
                          className="text-white btn btn-sm"
                          to={`/comic/${comic._id}/`}
                        >
                          {comic.title}
                        </Link>
                      </td>
                      <td>
                        <Link to={`/comic/${comic._id}/`}>
                          <Image fluid src={comic.images} alt={comic.title} />
                        </Link>
                      </td>

                      <td>
                        <LinkContainer
                          className="text-white btn btn-sm"
                          to={`/admin/comic/${comic._id}/edit`}
                        >
                          <Button variant="white" className="btn-sm">
                            <FaEdit /> Edit
                          </Button>
                        </LinkContainer>
                      </td>
                      <td>
                        <Button
                          variant="danger"
                          className="btn-sm"
                          onClick={() => deleteHandler(comic._id)}
                        >
                          <FaTrash /> Delete
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </Col>
          </Row>

          <Row>
            <Paginate
              pages={pages}
              page={page}
              isAdmin={true}
              keyword={keyword}
            />
          </Row>
        </Container>
      )}
    </Fragment>
  );
};

export default Comics;
