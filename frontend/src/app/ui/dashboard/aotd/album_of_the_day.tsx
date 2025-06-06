"use server"

import { Button } from "@heroui/react";

import AlbumDisplay from "./album_display";
import AlbumReviewBox from "./album_review_box";
import ReviewDisplay from "./review_display";
import { 
  getAlbumOfTheDayData, 
  getReviewsForAlbum, 
  getSimilarReviewsForRatings, 
  getAotdData, 
  getUserReviewForAlbum, 
} from "@/app/lib/aotd_utils";
import AddAlbumModal from "./modals/add_album_modal";

import Link from "next/link";
import { RiCalendar2Fill} from "react-icons/ri";
import { getUserData } from "@/app/lib/user_utils";

// GUI Display for the Album of the Day
export default async function AlbumOfTheDayBox(props) {
  // Get user Data
  const user_data = await getUserData()
  // Get album data
  const albumOfTheDayObj = await getAlbumOfTheDayData()
  const albumReview = await getUserReviewForAlbum(albumData("album_id"))
  const similarReviewData = await getSimilarReviewsForRatings(user_data['discord_id'])
  // Retrieve review data on this level instead of at reviewbox level
  let reviewList = await getReviewsForAlbum(albumData("album_id"));

  // Get Todays Date
  let todayDate = new Date()
  // Get yesterday's date
  const yesterdayString = new Date(new Date().setDate(new Date().getDate()-1)).toISOString().split('T')[0];
  const yesterdayStringArr = yesterdayString.split("-")

  // Pull data from album object, return empty string if not available
  function albumData(key) {
    if(key in albumOfTheDayObj) {
      return albumOfTheDayObj[key]
    } else { 
      return ''
    }
  }

  return (
    <div className="w-fit lg:max-w-[1080px] flex flex-col lg:flex-row lg:gap-2">
      <div className="backdrop-blur-2xl px-2 py-2 my-2 rounded-2xl bg-zinc-800/30 border border-neutral-800">
        <div className="w-full flex flex-col">
          <div className="flex w-full justify-between px-2 mt-1 mb-1">
            <Button 
              as={Link}
              href={`/dashboard/aotd/calendar/${yesterdayStringArr[0]}/${yesterdayStringArr[1]}/${yesterdayStringArr[2]}`}
              radius="lg"
              className={`w-fit hover:underline text-white bg-gradient-to-br from-green-700/80 to-green-800/80`}
              variant="solid"
            >
              <b>View Yesterday&apos;s Album</b>
            </Button>
            <Button 
              as={Link}
              href={`/dashboard/aotd/calendar/${todayDate.toISOString().split('T')[0].split("-")[0]}/${todayDate.toISOString().split('T')[0].split("-")[1]}`}
              radius="lg"
              className={`w-fit hover:underline text-white bg-gradient-to-br from-green-700/80 to-green-800/80`}
              variant="solid"
            >
              <RiCalendar2Fill className="text-2xl" />
            </Button> 
          </div>
          <AlbumDisplay 
            title={albumData("title")}
            disambiguation={albumData("disambiguation")}
            album_img_src={albumData("album_img_src")}
            album_id={albumData("album_id")}
            album_src={albumData("album_src")}
            album_mbid={albumData("album_id")}
            artist={albumData("artist")}
            submitter={albumData("submitter")}
            submitter_comment={albumData("submitter_comment")}
            submission_date={albumData("submission_date")}
            release_date={albumData("release_date")}
            release_date_precision={albumData("release_date_precision")}
            trackList={albumData("track_list")['tracks']}
          />
          <div className="w-full sm:w-3/4 mx-auto backdrop-blur-2xl px-2 py-2 my-2 rounded-2xl bg-black/20 border border-neutral-800">
            <p className="text-xs italic text-gray-300">
              All album artwork, track titles, artist names, and related content are the property of their respective copyright holders.
            </p>
          </div>
          <div className="w-full max-w-full">
            <AlbumReviewBox 
              album_id={albumData("album_id")}
              user_data={user_data}
              rating={(albumReview != null) ? albumReview['score'] : null}
              comment={(albumReview != null) ? albumReview['comment'] : null}
              first_listen={(albumReview != null) ? albumReview['first_listen']: null}
              similar_review_data={similarReviewData}
              hasUserSubmitted={(albumReview != null) ? albumReview['backendExist']: null}
            />
          </div>
          <div className="w-full flex">
            <AddAlbumModal />
          </div>
        </div>
      </div>
      <div className="static w-full lg:w-fit backdrop-blur-2xl px-2 py-2 mt-0 lg:my-2 rounded-2xl bg-zinc-800/30 border border-neutral-800">
        <ReviewDisplay 
          review_list={reviewList}
        />
      </div>
    </div>
  )
}