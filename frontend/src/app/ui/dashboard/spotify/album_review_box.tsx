'use client'

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { Button } from "@nextui-org/react";
import { Textarea } from "@nextui-org/input";
import { Slider, SliderValue, Select, SelectItem, Checkbox } from "@nextui-org/react";
import { submitReviewToBackend } from "@/app/lib/spotify_utils";


// GUI Display for an Album Review Box
// Expected Props:
//  - album_id: String - Album ID (spotify ID)
//  - song_data: List of Objects - List of songs included in the album
//      > name: String - Name of Song
//  - rating: Float - (optional) User rating if they left a previous review
//  - fav_song: String - (optional) Favorite song if they left a previous review
//  - comment: String - (optional) User's comment if they left a previous review
//  - first_listen: Boolean - (optional) Status of first listen if they left a previous review 
export default function AlbumReviewBox(props) {
  // Activate Router
  const router = useRouter();
  // State management
  const [rating, setRating] = useState<SliderValue>((props.rating != null) ? props.rating : 5);
  const [comment, setComment] = useState((props.comment != null) ? props.comment : "No Comment Provided");
  // const [favSong, setFavSong] = useState<Selection>(new Set([]));
  const [isReady, setIsReady] = useState(false);
  const [isFirstListen, setIsFirstListen] = useState((props.first_listen != null) ? props.first_listen : false);
  // Track if user has updated their review to be something different
  const [isReviewUpdated, setIsReviewUpdated] = useState(false);
  // Prop validation
  const songList = (props.song_data) ? props.song_data : [{name: "None Provided"}]

  const getSteps = () => {
    let steps: any = []
    for(let i = 0; i < 11; i++) {
      steps.push({
        value: i,
        label: `${i}`,
      })
    }
    return steps
  }

  // UseEffect to ensure review cannot be updated unless something changes
  useEffect(() => {
    if((rating != props.rating) || (comment != props.comment) || (isFirstListen != props.first_listen)) {
      setIsReviewUpdated(true)
    } else {
      setIsReviewUpdated(false)
    }
  }, [rating, comment, isFirstListen])

  // Send request to upload the submitted image
  const submitReview = () => {
    // Build out object
    let out = {}
    out['album_id'] = props.album_id
    out['score'] = rating
    out['comment'] = comment 
    out['first_listen'] = isFirstListen

    submitReviewToBackend(out)
    // Turn off review ready checkmark
    setIsReady(false)
    setIsReviewUpdated(false)
    // Reload page
    router.push("spotify")
  }

  return (
    <div className="w-full max-w-[1080px] px-2 lg:mx-auto py-2 flex flex-col rounded-xl bg-zinc-800/30 border border-neutral-800">
      <div className="w-full flex flex-col lg:flex-row gap-2 justify-between">
        <Slider   
          size="md"
          radius="lg"
          step={0.5}
          marks={getSteps()}
          color="warning"
          label="Album Rating"
          hideValue={true}
          maxValue={10} 
          minValue={0} 
          value={rating}
          onChange={setRating}
          className="max-w-full px-10 mx-auto" 
        />
        {/* <Select 
          label="Favorite Song" 
          className="max-w-full mx-auto my-auto" 
        >
          {songList.map((song) => (
            <SelectItem key={song.name}>
              {song.name}
            </SelectItem>
          ))}
        </Select> */}
      </div>
      <Textarea
        className="my-2"
        label="Comment (Not Required)"
        minRows={1}
        description="Enter an optional comment to go with your review of this album."
        value={comment}
        onValueChange={setComment}
      />
      <div className="w-full flex flex-col lg:flex-row gap-2 justify-between">
        <Checkbox
          isSelected={isFirstListen}
          onValueChange={setIsFirstListen}
        >
          First Time Listen?
        </Checkbox>
        <div className="flex flex-col gap-1 ">
          <Checkbox
            isSelected={isReady}
            onValueChange={setIsReady}
            isDisabled={!isReviewUpdated}
          >
            Ready to {(props.rating != null)? "Update" : "Submit"}?
          </Checkbox>
          <Button
            isDisabled={!isReady}
            onPress={submitReview}
          >
            {(props.rating != null)? "Update" : "Submit"} Review
          </Button>
        </div>
      </div>
    </div>
  );
}