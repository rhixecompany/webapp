import React, { Fragment, useEffect } from "react";

import { useDispatch, useSelector } from "react-redux";
import { listComicDetails } from "../../actions/comicsActions";
import Loader from "../../components/features/Loader";
import Message from "../../components/features/Message";
import Rating from "../../components/features/Rating";
import { ListGroup, Container, Row, Col, Image } from "react-bootstrap";
import { Link } from "react-router-dom";

const Comic = ({ match }) => {
  const comicId = match.params.id;

  const dispatch = useDispatch();
  const { comic, error, loading, chapters } = useSelector(
    (state) => state.comicDetails
  );
  useEffect(() => {
    dispatch(listComicDetails(comicId));
  }, [dispatch, comicId]);
  return (
    <Fragment>
      {loading ? (
        <Loader />
      ) : error ? (
        <Message variant="danger">{error}</Message>
      ) : (
        <Container>
          <Row>
            <Col md={3}>
              <div>
                <Image
                  fluid
                  className="img-fluid"
                  src={comic?.images}
                  alt={comic?.title}
                />
              </div>
              <div>
                <div>
                  {" "}
                  <strong>Status:</strong>
                  <span>{comic?.status}</span>
                </div>

                <div>
                  {" "}
                  <strong>Type:</strong>
                  <Link to={`/category/${comic?.category?._id}/`}>
                    {comic?.category?.name}
                  </Link>
                </div>
                <div>
                  <Rating
                    value={comic?.rating}
                    text={`${comic?.rating} Rating`}
                    color={"#f8e825"}
                  />
                </div>
              </div>
            </Col>
            <Col md={6}>
              <div>
                <h1>{comic?.title}</h1>
              </div>
              <div>
                <strong>Genres:</strong>
                {comic?.genres?.length > 0 ? (
                  <ListGroup variant="flush">
                    {comic?.genres?.map((genre) => {
                      return (
                        <ListGroup.Item key={genre._id}>
                          <Link to={`/genre/${genre._id}/`}>{genre.name}</Link>
                        </ListGroup.Item>
                      );
                    })}
                  </ListGroup>
                ) : (
                  <Message variant="info">{<small>No Genres</small>}</Message>
                )}
              </div>
              <div>
                {" "}
                <strong>Plot:</strong>
                <p> {comic?.description}</p>
              </div>
              <div>
                {" "}
                <strong>Alternativetitle:</strong>
                <span>{comic?.alternativetitle}</span>
              </div>

              <div>
                {" "}
                <strong>Author:</strong>
                <span>{comic?.author}</span>
              </div>
              <div>
                {" "}
                <strong>Artist:</strong>
                <span>{comic?.artist}</span>
              </div>
              <div>
                {" "}
                <strong>Released:</strong>
                <span> {comic?.released}</span>
              </div>
              <div>
                {" "}
                <strong>Serialization:</strong>
                <span>{comic?.serialization}</span>
              </div>
              <div>
                {" "}
                <strong>Updated:</strong>
                <time> {new Date(comic?.updated).toLocaleString("en-US")}</time>
              </div>
              <div>
                {" "}
                <strong>Published:</strong>
                <time> {new Date(comic?.publish).toLocaleString("en-US")}</time>
              </div>
            </Col>
          </Row>
          <Row>
            <Col>
              {chapters?.length > 0 ? (
                <ListGroup variant="flush">
                  {chapters?.map((chapter) => {
                    return (
                      <ListGroup.Item key={chapter._id}>
                        <strong>Name:</strong>
                        <Link to={`/chapter/${chapter._id}/`}>
                          {chapter.name}
                        </Link>
                      </ListGroup.Item>
                    );
                  })}
                </ListGroup>
              ) : (
                <Message variant="info">{<small>No Chapter</small>}</Message>
              )}
            </Col>
          </Row>
        </Container>
      )}
    </Fragment>
  );
};

export default Comic;
