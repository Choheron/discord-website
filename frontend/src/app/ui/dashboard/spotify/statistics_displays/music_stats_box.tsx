'use server'

import UserCard from "@/app/ui/general/userUiItems/user_card";
import { getAlbumAvgRating, getAlbumsStats, getAllUserReviewStats, getLowestHighestAlbumStats } from "@/app/lib/spotify_utils";
import AlbumDisplay from "../album_display";

import {Badge} from "@nextui-org/badge";
import { Divider } from "@nextui-org/react";
import { ratingToTailwindBgColor } from "@/app/lib/utils";
import ReviewStatsUserCard from "./review_stats_user_card";

// GUI Display for an Album
// Expected Props:
//   - NONE YET
export default async function MusicStatsBox(props) {
  const albumStatsJson = await getAlbumsStats();
  const albumLowHighStatsJson = await getLowestHighestAlbumStats();
  const userReviewStatsJson = await getAllUserReviewStats();

  const albumUserStatsList = albumStatsJson['user_objs'].sort((a, b) => a['submission_count'] < b['submission_count'] ? 1 : -1).map((user, index) => {
    return (
      <div 
        key={user['submission_count']}
        className="flex justify-between w-full my-1"
      >
        <UserCard
          userDiscordID={user['discord_id']}
        />
        <p className="my-auto px-2 py-1 bg-gray-800 rounded-full">
          {user['submission_count']}
        </p>
      </div>
    )
  })

  const reviewUserStatsList = userReviewStatsJson['review_data'].sort((a, b) => a['total_reviews'] < b['total_reviews'] ? 1 : -1).map((user) => {
    return (
      <div 
        key={`${user['discord_id']}-${user['total_reviews']}`}
        className="flex justify-between w-full my-1"
      >
        <ReviewStatsUserCard userDiscordID={user['discord_id']} userReviewObj={user}/>
        <p className="my-auto px-2 py-1 bg-gray-800 rounded-full">
          {user['total_reviews']}
        </p>
      </div>
    )
  })

  return (
    <div className="w-fill min-w-[340px] mx-2 lg:mx-0 my-2 px-2 py-2 flex flex-col lg:flex-row gap-10 backdrop-blur-2xl rounded-2xl bg-zinc-800/30 border border-neutral-800">
      {/* Album Submission Stats */}
      <div className='min-w-[300px] w-fit mx-auto flex flex-col'>
        <p className="mx-auto text-xl underline mb-1">
          Album Submission Stats: 
        </p>
        <div className="flex gap-2 justify-between w-full">
          <p>
            Total Albums Submitted:
          </p>
          <p>
            {albumStatsJson['total_albums']}
          </p>
        </div>
        <Divider className="my-1" />
        {albumUserStatsList}
      </div>
      {/* Lowest and Highest Album Stats */}
      <div className="flex flex-col">
        {/* Album Highest Stats */}
        <div className='min-w-[300px] w-fit mx-auto flex flex-col'>
          <p className="mx-auto text-xl underline mb-2">
            Highest Album: {albumLowHighStatsJson['highest_album']['date']}
          </p>
          <Badge 
            content={(await getAlbumAvgRating(albumLowHighStatsJson['highest_album']["spotify_id"], false)).toFixed(2)} 
            size="lg" 
            placement="top-left" 
            shape="rectangle"
            showOutline={false}
            variant="shadow"
            className={`lg:-ml-4 -mt-1 ${ratingToTailwindBgColor((await getAlbumAvgRating(albumLowHighStatsJson['highest_album']["spotify_id"], false)).toFixed(2))} lg:text-xl text-black`}
          >
            <AlbumDisplay
              title={albumLowHighStatsJson['highest_album']["title"]}
              album_spotify_id={albumLowHighStatsJson['highest_album']["spotify_id"]}
              album_img_src={albumLowHighStatsJson['highest_album']["album_img_src"]}
              album_src={albumLowHighStatsJson['highest_album']["spotify_url"]}
              artist={{"name": albumLowHighStatsJson['highest_album']["artist"], "href": albumLowHighStatsJson['highest_album']["artist_url"]}}
              submitter={albumLowHighStatsJson['highest_album']["submitter_id"]}
              submitter_comment={albumLowHighStatsJson['highest_album']["submitter_comment"]}
              submission_date={albumLowHighStatsJson['highest_album']["submission_date"]}
              historical_date={albumLowHighStatsJson['highest_album']['date']}
            />
          </Badge>
          <Divider className="my-1" />
        </div>
        {/* Album Lowest Stats */}
        <div className='min-w-[300px] w-fit mx-auto flex flex-col'>
          <p className="mx-auto text-xl underline mb-2">
            Lowest Album: {albumLowHighStatsJson['lowest_album']['date']}
          </p>
          <Badge 
            content={(await getAlbumAvgRating(albumLowHighStatsJson['lowest_album']["spotify_id"], false)).toFixed(2)} 
            size="lg" 
            placement="top-left" 
            shape="rectangle"
            showOutline={false}
            variant="shadow"
            className={`lg:-ml-4 -mt-1 ${ratingToTailwindBgColor((await getAlbumAvgRating(albumLowHighStatsJson['lowest_album']["spotify_id"], false)).toFixed(2))} lg:text-xl text-black`}
          >
            <AlbumDisplay
              title={albumLowHighStatsJson['lowest_album']["title"]}
              album_spotify_id={albumLowHighStatsJson['lowest_album']["spotify_id"]}
              album_img_src={albumLowHighStatsJson['lowest_album']["album_img_src"]}
              album_src={albumLowHighStatsJson['lowest_album']["spotify_url"]}
              artist={{"name": albumLowHighStatsJson['lowest_album']["artist"], "href": albumLowHighStatsJson['lowest_album']["artist_url"]}}
              submitter={albumLowHighStatsJson['lowest_album']["submitter_id"]}
              submitter_comment={albumLowHighStatsJson['lowest_album']["submitter_comment"]}
              submission_date={albumLowHighStatsJson['lowest_album']["submission_date"]}
              historical_date={albumLowHighStatsJson['lowest_album']['date']}
            />
          </Badge>
        </div>
        <div className="max-w-[320px] lg:max-w-[650px] px-2 py-2 mt-2 text-small italic border border-neutral-800 rounded-2xl bg-zinc-800/30">
          <p>In order to be considered for highest or lowest album, an album must have 4 or more reviews. Any album with 3 or less reviews will not be counted.</p>
        </div>
      </div>
      {/* Review Stats */}
      <div className='min-w-[320px] w-fit mx-auto flex flex-col'>
        <p className="mx-auto text-xl underline mb-1">
          Review Stats: 
        </p>
        <div className="flex gap-2 justify-between w-full">
          <p>
            Total Reviews Submitted:
          </p>
          <p>
            {userReviewStatsJson['total_reviews']}
          </p>
        </div>
        <Divider className="my-1" />
        {reviewUserStatsList}
      </div>
    </div>
  )
}