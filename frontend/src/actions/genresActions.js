import axios from "axios";
import {
  GENRES_LIST_REQUEST,
  GENRES_LIST_SUCCESS,
  GENRES_LIST_FAIL,
  GENRES_DETAILS_REQUEST,
  GENRES_DETAILS_SUCCESS,
  GENRES_DETAILS_FAIL,
} from "../constants/genresConstants";

export const listGenres = () => async (dispatch) => {
  try {
    dispatch({ type: GENRES_LIST_REQUEST });

    const { data } = await axios.get(`/api/genres/`);

    dispatch({
      type: GENRES_LIST_SUCCESS,
      payload: data,
    });
    //console.log(data);
  } catch (error) {
    dispatch({
      type: GENRES_LIST_FAIL,
      payload:
        error.response && error.response.data.detail
          ? error.response.data.detail
          : error.message,
    });
  }
};

export const listGenreDetails = (id) => async (dispatch) => {
  try {
    dispatch({ type: GENRES_DETAILS_REQUEST });

    const { data } = await axios.get(`/api/genres/${id}/`);

    dispatch({
      type: GENRES_DETAILS_SUCCESS,
      payload: data,
    });
    //console.log(data);
  } catch (error) {
    dispatch({
      type: GENRES_DETAILS_FAIL,
      payload:
        error.response && error.response.data.detail
          ? error.response.data.detail
          : error.message,
    });
  }
};
