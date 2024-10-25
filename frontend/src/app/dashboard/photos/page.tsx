import PhotoModal from "@/app/ui/dashboard/photos/photo_modal";
import PageTitle from "@/app/ui/dashboard/page_title";
import UploadPhotoModal from "@/app/ui/dashboard/photos/upload_photo_modal";

import { getAllPhotoshops } from "@/app/lib/photos_utils";

export default async function photos() {
  async function loadImages(imageDir: string) {
    const fileListString: any = await getAllPhotoshops();
    const fileList = fileListString.split(',')
    // Cut list into 3 different columns (into a terribly named var)
    var fileListList: any[] = [[],[],[]]
    var step = fileList.length/3;
    for (let i = 0; i < fileList.length; i++) {
      if(i < step) {
        fileListList[0].push(fileList[i])
      }else if(i < step*2) {
        fileListList[1].push(fileList[i])
      } else {
        fileListList[2].push(fileList[i])
      }
    }    

    return (
      <div className="flex gap-6 w-3/4">
        { fileListList.map((list: string[], listIndex: number) => (
          <div key={listIndex} className="w-full flex flex-col gap-6 items-center pt-3">
            { list.map((id: string, index: number) => (
              <PhotoModal
                key={index}
                imageSrc={`${process.env.NEXT_PUBLIC_BASE_BACKEND_URL}/photos/image/${id}`}
                nameString={`Photo ${id}`}
              />
            ))}
          </div>
        ))}
      </div>
    );
  }

  return (
    <main className="flex min-h-screen flex-col items-center p-24 pt-10">
      <PageTitle text="Photoshops" />
      <UploadPhotoModal />
      {loadImages(`${process.env.NEXT_PUBLIC_PHOTOSHOP_DIRECTORY}`)}
    </main>
  );
}
