import React, { Fragment, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import Loader from "../../components/features/Loader";
import Message from "../../components/features/Message";

import { listChapterDetails } from "../../actions/chaptersActions";
import {
  NavDropdown,
  ListGroup,
  Container,
  Image,
  Row,
  Col,
} from "react-bootstrap";
import { Link } from "react-router-dom";
import { LinkContainer } from "react-router-bootstrap";

const Chapter = ({ match }) => {
  const chapterId = match.params.id;

  const dispatch = useDispatch();
  const chapterDetails = useSelector((state) => state.chapterDetails);
  const { chapter, error, loading, pages, comic, chapters } = chapterDetails;

  useEffect(() => {
    dispatch(listChapterDetails(chapterId));
  }, [dispatch, chapterId]);
  return (
    <Fragment>
      {loading ? (
        <Loader />
      ) : error ? (
        <Message variant="danger">{error}</Message>
      ) : (
        <Container fluid>
          <Row>
            <Col>
              {" "}
              <ListGroup>
                <ListGroup.Item>
                  <Link to={`/comic/${comic?._id}/`}>{comic?.title}</Link>
                </ListGroup.Item>
                <ListGroup.Item>
                  <NavDropdown title={chapter?.name} id="username">
                    {chapters?.map((chap) => {
                      return (
                        <LinkContainer
                          key={chap._id}
                          to={`/chapter/${chap?._id}/`}
                        >
                          <NavDropdown.Item>{chap.name}</NavDropdown.Item>
                        </LinkContainer>
                      );
                    })}
                  </NavDropdown>
                </ListGroup.Item>
              </ListGroup>
            </Col>
          </Row>
          {pages?.length > 0 ? (
            <>
              {pages?.map((page) => (
                <div key={page._id}>
                  <Image
                    className="img-fluid"
                    src={page.images}
                    alt={page.images}
                  />
                </div>
              ))}
            </>
          ) : (
            <Message variant="danger">{<small>No Pages</small>}</Message>
          )}
          <Row>
            <Col>
              <ListGroup>
                <ListGroup.Item>
                  <Link to={`/comic/${comic?._id}/`}>{comic?.title}</Link>
                </ListGroup.Item>
                <ListGroup.Item>
                  <NavDropdown title={chapter?.name} id="username">
                    {chapters?.map((chap) => {
                      return (
                        <LinkContainer
                          key={chap._id}
                          to={`/chapter/${chap?._id}/`}
                        >
                          <NavDropdown.Item>{chap.name}</NavDropdown.Item>
                        </LinkContainer>
                      );
                    })}
                  </NavDropdown>
                </ListGroup.Item>
              </ListGroup>
            </Col>
          </Row>
        </Container>
      )}
    </Fragment>
  );
};

export default Chapter;
