import React, { useEffect, Fragment } from "react";
import Loader from "../../components/features/Loader";
import Message from "../../components/features/Message";
import ChapterPaginate from "../../components/features/ChapterPaginate";
import { useDispatch, useSelector } from "react-redux";
import { listChapters, deleteChapter } from "../../actions/chaptersActions";

import { Table, Button, Container, Row, Col } from "react-bootstrap";
import { FaEdit, FaTrash, FaPlus } from "react-icons/fa";
import { Link } from "react-router-dom";
import { LinkContainer } from "react-router-bootstrap";
const Chapters = ({ history }) => {
  let keyword = history.location.search;
  const dispatch = useDispatch();
  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;
  const chaptersList = useSelector((state) => state.chaptersList);
  const { chapters, error, loading, pages, page, count } = chaptersList;
  const chapterDelete = useSelector((state) => state.chapterDelete);
  const {
    loading: loadingDelete,
    error: errorDelete,
    success: successDelete,
  } = chapterDelete;
  useEffect(() => {
    if (!userInfo || !userInfo.isAdmin) {
      history.push("/login");
    }
    dispatch(listChapters(keyword));
  }, [userInfo, history, dispatch, keyword, successDelete]);
  const deleteHandler = (name) => {
    if (window.confirm(`Are you sure you want to delete:${name}`)) {
      dispatch(deleteChapter(name));
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
              <h2>Total Chapters:{count}</h2>
            </Col>
            <Col className="text-right">
              <Button variant="secondary">
                <Link to={"/admin/chapter/create"}>
                  <FaPlus /> Create New Chapter
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
                    <th>Name</th>

                    <th>numPages</th>

                    <th></th>
                    <th></th>
                  </tr>
                </thead>

                <tbody>
                  {chapters?.map((chapter) => (
                    <tr key={chapter._id}>
                      <td>
                        <Link
                          className="text-white btn btn-sm"
                          to={`/chapter/${chapter._id}/`}
                        >
                          {chapter.name}
                        </Link>
                      </td>

                      <td>{chapter.numPages}</td>

                      <td>
                        <LinkContainer
                          className="text-white btn btn-sm"
                          to={`/admin/chapter/${chapter._id}/edit`}
                        >
                          <Button variant="white" className="btn-sm">
                            Edit <FaEdit />
                          </Button>
                        </LinkContainer>
                      </td>
                      <td>
                        <Button
                          variant="danger"
                          className="btn-sm"
                          onClick={() => deleteHandler(chapter._id)}
                        >
                          Delete <FaTrash />
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </Col>
          </Row>
          <Row className="align-items-center">
            <ChapterPaginate
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

export default Chapters;
