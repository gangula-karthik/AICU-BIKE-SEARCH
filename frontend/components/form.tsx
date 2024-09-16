"use client"

import React, { useState } from 'react';
import { Tabs, Tab, Card, CardBody, Textarea, Button } from '@nextui-org/react';
import { toast } from 'sonner';
import { InboxOutlined } from '@ant-design/icons';
import { Upload, message } from 'antd';
import BikeCard from './BikeCard';
import axios from 'axios';
const { Dragger } = Upload;

interface UploadProps {
  name: string;
  multiple: boolean;
  customRequest: (options: {
    onSuccess: (file: File) => void;
    onError: (error: Error) => void;
    file: File;
    onProgress: (percent: number) => void;
  }) => void;
  onChange: (info: {
    file: File;
    fileList: File[];
    status: string;
  }) => void;
  onDrop: (e: React.DragEvent<HTMLDivElement>) => void;
}

export default function App() {
  const [prompt, setPrompt] = useState<string>("");
  const [bikes, setBikes] = useState<{ metadatas: any[], documents: any[] }>({ metadatas: [], documents: [] });

  const uploadProps: UploadProps = {
    name: 'file',
    multiple: true,
    customRequest: async (options) => {
      const { onSuccess, onError, file, onProgress } = options;
      
      const formData = new FormData();
      formData.append('file', file); 
      
      try {
        const response = await axios.post('http://127.0.0.1:8000/process_image/', formData, {
          onUploadProgress: ({ total, loaded }) => {
            if (total) {
              onProgress(Math.round((loaded / total) * 100));
            }
          },
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        setBikes(response.data.results); 
        onSuccess(file); 
      } catch (error) {
        console.error('Upload failed:', error);
        if (error instanceof Error) {
          onError(error);
          message.error('Upload failed: ' + error.message);
        } else {
          onError(new Error(String(error)));
          message.error('Upload failed');
        }
      }
    },
    onChange(info) {
      const { status } = info;
      if (status !== 'uploading') {
        console.log(info.file, info.fileList);
      }
      if (status === 'done') {
        message.success(`${info.file.name} file uploaded successfully.`);
      } else if (status === 'error') {
        message.error(`${info.file.name} file upload failed.`);
      }
    },
    onDrop(e) {
      console.log('Dropped files', e.dataTransfer.files);
    },
  };

  const handleSubmitText = async () => {
    try {
      const queryParams = new URLSearchParams({ text: prompt }).toString();
      if (!prompt.trim()) {
        toast.error("Please enter some text before submitting.");
        return;
      }
      const url = `http://127.0.0.1:8000/process_text/?${queryParams}`;

      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'accept': 'application/json',
        },
      });
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

      const data = await response.json();
      console.log(data);
      setBikes(data.results);
      toast.success('Text submitted successfully.');
    } catch (error: any) {
      console.error('Failed to submit text:', error);
      toast.error(`Failed to submit text: ${error.message}`);
    }
  };

  let tabs = [
    {
      id: "text",
      label: "✏️ Text Input",
      content: (
        <div className="flex flex-col gap-3">
          <Textarea
            value={prompt}
            onChange={(e) => setPrompt(e.currentTarget.value)}
            fullWidth
            placeholder="Prompt E.g.: 'White color HITO X4 FOLDING BIKE in excellent condition, featuring a lightweight aluminum frame and hydraulic disc brakes.'"
          />
          <Button onClick={handleSubmitText} color="primary">
            Submit Text
          </Button>
        </div>
      ),
    },
    {
      id: "image",
      label: "📷 Image Upload",
      content: (
        <div className="flex flex-col gap-3 items-center justify-center">
          <Dragger {...uploadProps}>
            <p className="ant-upload-drag-icon">
              <InboxOutlined />
            </p>
            <p className="ant-upload-text">Click or drag file to this area to upload</p>
            <p className="ant-upload-hint">
              Support for a single or bulk upload. Strictly prohibited from uploading company data or other
              banned files.
            </p>
          </Dragger>
        </div>
      ),
    },
  ];

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
          <div className="flex w-full flex-col min-h-[290px] pt-4">
            <Tabs aria-label="Content tabs" color="primary" variant="light" size="sm" radius='full'>
              {tabs.map((tab) => (
                <Tab key={tab.id} title={tab.label}>
                  <Card>
                    <CardBody>{tab.content}</CardBody>
                  </Card>
                </Tab>
              ))}
            </Tabs>
          </div>
        </div>
      </div>
      <div className="w-full px-4">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-9">
          {
            bikes.metadatas && bikes.metadatas[0] && bikes.documents && bikes.documents[0] && bikes.metadatas[0].length > 0 ? (
              bikes.metadatas[0].map((metadata: { product_name?: any; image_url?: any; source?: any; }, index: string | number) => {
                const fullDescription = bikes.documents[0][index];
                const description = fullDescription.length > 100 ? `${fullDescription.substring(0, 100)}...` : fullDescription;

                const fullBikeName = metadata.product_name;
                // const bikeName = fullBikeName.length > 10 ? `${fullBikeName.substring(0, 100)}...` : fullBikeName;

                const { image_url: imageUrl, source } = metadata;

                return (
                  <BikeCard
                    key={source}
                    imageUrl={imageUrl}
                    bikeName={fullBikeName}
                    description={description}
                    source={source}
                  />
                );
              })
            ) : (
              <p>No bikes available.</p>
            )
          }

        </div>
      </div>
    </div>
  );
}
