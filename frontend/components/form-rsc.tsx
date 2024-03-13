import Form from "@/components/form";
import { Suspense } from "react";
import BikeCard from '@/components/BikeCard';
import { Card, CardHeader, CardBody, CardFooter, Image, Button, Chip } from "@nextui-org/react";


export default function FormRSC({
  prompt,
  pattern,
  image,
}: {
  prompt?: string;
  pattern?: string;
  image: string | null;
}) {
  return (
    <div className="flex flex-col items-center">
      <div className="z-10 w-full max-w-xl px-2.5 xl:px-0 text-center">
        <h1
          className="animate-fade-up bg-gradient-to-br from-black to-stone-500 bg-clip-text font-display text-4xl font-bold tracking-[-0.02em] text-transparent opacity-0 drop-shadow-sm md:text-7xl md:leading-[5rem]"
          style={{ animationDelay: "0.15s", animationFillMode: "forwards" }}
        >
          AICU BIKE SEARCH
        </h1>
        <p
          className="mt-6 animate-fade-up text-gray-500 opacity-0 md:text-xl"
          style={{ animationDelay: "0.25s", animationFillMode: "forwards" }}
        >
          Never lose your bicycle again. Powered by{" "}
          <a
            className="text-black underline-offset-4 hover:underline"
            href="https://openai.com/research/clip"
            target="_blank"
            rel="noopener noreferrer"
          >
            CLIP
          </a>{" "}
          and{" "}
          <a
            className="text-black underline-offset-4 hover:underline"
            href="https://www.trychroma.com/"
            target="_blank"
            rel="noopener noreferrer"
          >
            ChromaDB
          </a>
          .
        </p>
        <div className="mb-8">
          <Form promptValue={prompt} patternValue={pattern} />
        </div>
      </div>
      <div className="w-full px-4">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-9">
          <BikeCard
            imageUrl="https://media.karousell.com/media/photos/products/2024/3/11/santa_cruz_blur_c_size_l_1710170584_6909f8ff_progressive.jpg"
            bikeName="Bicycle Foldable Bike"
            description="All in good condition! Used a few times only. Can test ride."
          />
          <BikeCard
            imageUrl="https://media.karousell.com/media/photos/products/2024/3/11/santa_cruz_blur_c_size_l_1710170584_6909f8ff_progressive.jpg"
            bikeName="Bicycle Foldable Bike"
            description="All in good condition! Used a few times only. Can test ride."
          />
          <BikeCard
            imageUrl="https://media.karousell.com/media/photos/products/2024/3/11/santa_cruz_blur_c_size_l_1710170584_6909f8ff_progressive.jpg"
            bikeName="Bicycle Foldable Bike"
            description="All in good condition! Used a few times only. Can test ride."
          />
        </div>
      </div>
    </div>
  );
}