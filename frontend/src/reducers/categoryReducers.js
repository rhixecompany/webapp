import {
  CATEGORY_LIST_REQUEST,
  CATEGORY_LIST_SUCCESS,
  CATEGORY_LIST_FAIL,
  CATEGORY_DETAILS_REQUEST,
  CATEGORY_DETAILS_SUCCESS,
  CATEGORY_DETAILS_FAIL,
} from "../constants/categoryConstants";

export const categorysListReducer = (state = {}, action) => {
  switch (action.type) {
    case CATEGORY_LIST_REQUEST:
      return { loading: true };

    case CATEGORY_LIST_SUCCESS:
      return { ...state, loading: false, categorys: action.payload.result };

    case CATEGORY_LIST_FAIL:
      return { loading: false, error: action.payload };

    default:
      return state;
  }
};

export const categoryDetailsReducer = (state = {}, action) => {
  switch (action.type) {
    case CATEGORY_DETAILS_REQUEST:
      return { loading: true };

    case CATEGORY_DETAILS_SUCCESS:
      return {
        ...state,
        loading: false,
        category: action.payload.result,
        comics: action.payload.comics,
      };

    case CATEGORY_DETAILS_FAIL:
      return { loading: false, error: action.payload };

    default:
      return state;
  }
};
