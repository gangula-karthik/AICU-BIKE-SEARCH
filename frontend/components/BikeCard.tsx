"use client"

interface BikeCardProps {
    imageUrl: string;
    bikeName: string;
    description: string;
  }

  
import React from 'react';
import { Card, CardHeader, CardFooter, Image, Button, Chip } from '@nextui-org/react';

const BikeCard: React.FC<BikeCardProps> = ({ imageUrl, bikeName, description }) => {
  return (
    <Card isFooterBlurred className="w-[400px] h-[250px]">
      <CardHeader className="absolute z-10 top-1 flex-col items-start">
        <Chip color="primary">
          <h4 className="text-white/90">{bikeName}</h4>
        </Chip>
      </CardHeader>
      <Image
        removeWrapper
        alt={bikeName}
        className="z-0 w-full h-full object-cover"
        src={imageUrl}
      />
      <CardFooter className="absolute bg-black/40 bottom-0 z-10 border-t-1 border-default-600">
        <div className="flex flex-grow gap-2 items-center">
          <div className="flex flex-col">
            <p className="text-tiny text-white/60">{description}</p>
          </div>
        </div>
        <Button color="primary" radius="full" size="sm">View It 🚀</Button>
      </CardFooter>
    </Card>
  );
};

export default BikeCard;