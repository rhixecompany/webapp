import React, { Fragment, useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { listComicDetails, updateComic } from "../../actions/comicsActions";
import Loader from "../../components/features/Loader";
import Message from "../../components/features/Message";
import { Link } from "react-router-dom";
import { Form, Button, Container } from "react-bootstrap";
import { COMICS_UPDATE_RESET } from "../../constants/comicsConstants";
import FormContainer from "../../components/features/FormContainer";
import axios from "axios";
const ComicEdit = ({ match, history }) => {
  const comicId = match.params.id;

  const [title, setTitle] = useState("");
  const [images, setImages] = useState("");
  const [uploading, setUploading] = useState(false);

  const dispatch = useDispatch();

  const { comic, error, loading } = useSelector((state) => state.comicDetails);
  const comicUpdate = useSelector((state) => state.comicUpdate);
  const {
    error: errorUpdate,
    loading: loadingUpdate,
    success: successUpdate,
  } = comicUpdate;
  useEffect(() => {
    if (successUpdate) {
      dispatch({ type: COMICS_UPDATE_RESET });
      history.push("/admin/comicslist");
    } else {
      if (!comic?.title || comic?._id !== Number(comicId)) {
        dispatch(listComicDetails(comicId));
      } else {
        setTitle(comic?.title);
        setImages(comic?.images);
      }
    }
  }, [dispatch, comic, comicId, history, successUpdate]);

  const onSubmit = (e) => {
    e.preventDefault();

    dispatch(
      updateComic({
        _id: comicId,
        title,
      })
    );
  };

  const uploadFileHandler = async (e) => {
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append("image", file);
    formData.append("comic_Id", comicId);
    setUploading(true);
    try {
      const config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };

      const { data } = await axios.post(
        "/api/comics/upload/",
        formData,
        config
      );

      setImages(data);
      setUploading(false);
    } catch (error) {
      setUploading(false);
    }
  };

  return (
    <Fragment>
      <Link className="btn btn-sm" to={"/admin/comicslist"}>
        Go Back
      </Link>
      <FormContainer>
        <h1>Edit Comic</h1>
        {loadingUpdate && <Loader />}
        {errorUpdate && <Message variant="danger">{errorUpdate}</Message>}

        {loading ? (
          <Loader />
        ) : error ? (
          <Message variant="danger">{error}</Message>
        ) : (
          <Container>
            <Form onSubmit={onSubmit}>
              <Form.Group controlId="title">
                <Form.Label>Title</Form.Label>
                <Form.Control
                  required
                  type="title"
                  placeholder="Enter title"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                ></Form.Control>
              </Form.Group>
              <Form.Group controlId="images">
                <Form.Label>Images</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Enter images"
                  value={images}
                  onChange={(e) => setImages(e.target.value)}
                ></Form.Control>

                <Form.File
                  multiple
                  id="image-file"
                  label="Choose Image"
                  custom
                  onChange={uploadFileHandler}
                ></Form.File>
                {uploading && <Loader />}
              </Form.Group>

              <Button type="submit" variant="primary">
                Update
              </Button>
            </Form>
          </Container>
        )}
      </FormContainer>
    </Fragment>
  );
};

export default ComicEdit;
