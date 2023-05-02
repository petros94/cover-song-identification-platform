import axios from "axios"
import { sortByKey } from 'utils/generic'

const API_URL = '/api';
const ax = axios.create({ baseURL: API_URL })

/**
 * Retrieve songs count
 * 
 * @returns json in the form:
 *  {
 *      "count": integer
 *  }
 */
const getSongsCount = () => {
    return ax({
        url: "/songs/count",
        method: "GET"
    })
        .then(res => res.data)
}

/**
 * Retrieve songs count
 * 
 * @returns json in the form:
 *  {
 *      "count": integer
 *  }
 */
const getAllSongs = () => {
    return ax({
        url: "/songs",
        method: "GET"
    })
        .then(res => res.data)
        .then(songs => sortByKey(songs, 'title'))
}

const getSong = (id) => {
    return ax({
        url: `/songs/${id}`,
        method: "GET"
    })
        .then(res => res.data)
}

/**
 * 
 * @param {str} yt_link 
 * @returns 
 */
const postSong = ({ yt_link }) => {
    return ax({
        url: "/songs",
        method: "POST",
        data: {
            'yt_link': yt_link
        }
    })
        .then(res => res.data)
}

 const deleteSong = (id) => {
    return ax({
        url: `/songs/${id}`,
        method: "DELETE"
    })
        .then(res => res.data)
}

const predictPair = (song1, song2) => {
    return ax({
        url: `/predict/pair?id_1=${song1}&id_2=${song2}`,
        method: "GET"
    }).then(res => res.data)
}

const predictRank = (song1) => {
    return ax({
        url: `/predict/rank?id_1=${song1}`,
        method: "GET"
    }).then(res => res.data)
}

const predictRankAggregated = (song1) => {
    return ax({
        url: `/predict/rankaggregated?id_1=${song1}`,
        method: "GET"
    }).then(res => res.data)
}

export { getSongsCount, getAllSongs, getSong, postSong, deleteSong, predictPair, predictRank, predictRankAggregated }