import React, { useState } from "react";
import {
  Card,
  CardContent,
  Typography,
  Box,
  IconButton,
  Divider,
} from "@mui/material";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import DocumentItem from "./DocumentItem";

function SourceCard({ source, documents, threadId }) {
  const [pageIndex, setPageIndex] = useState(0);
  const itemsPerPage = 8;

  const handlePageChange = (direction) => {
    setPageIndex((prev) =>
      Math.max(
        0,
        Math.min(
          documents.length - itemsPerPage,
          prev + direction * itemsPerPage,
        ),
      ),
    );
  };

  return (
    <Card
      sx={{
        borderRadius: 0,
        boxShadow: 0,
        overflow: "hidden",
        display: "flex",
        flexDirection: "column",
        background: "primary.main",
      }}
    >
      <Divider />
      <CardContent sx={{ p: 0 }}>
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            bgcolor: "background.paper",
          }}
        >
          {documents
            .slice(pageIndex, pageIndex + itemsPerPage)
            .map((document, index) => (
              <DocumentItem
                key={`${document.metadata.id}-${pageIndex + index}`}
                document={document}
                threadId={threadId}
              />
            ))}
        </Box>
      </CardContent>
      <Divider />
      <Box
        sx={{
          p: 0,
          bgcolor: "background.paper",
          borderRadius: 0,
          boxShadow: 0,
        }}
      >
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <IconButton
            onClick={() => handlePageChange(-1)}
            disabled={pageIndex === 0}
            size="small"
            sx={{ color: "primary.main" }}
          >
            <ChevronLeftIcon />
          </IconButton>
          <Typography variant="caption" sx={{ color: "text.secondary" }}>
            {`${pageIndex + 1} - ${Math.min(pageIndex + itemsPerPage, documents.length)} of ${documents.length}`}
          </Typography>
          <IconButton
            onClick={() => handlePageChange(1)}
            disabled={pageIndex + itemsPerPage >= documents.length}
            size="small"
            sx={{ color: "primary.main" }}
          >
            <ChevronRightIcon />
          </IconButton>
        </Box>
      </Box>
    </Card>
  );
}

export default SourceCard;
