import React, { useState } from "react";
import {
  Typography,
  Box,
  IconButton,
  Link,
  Collapse,
  Tooltip,
  Chip,
  Paper,
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import HelpOutlineIcon from "@mui/icons-material/HelpOutline";
import CloseIcon from "@mui/icons-material/Close";
import ExplanationBox from "./ExplanationBox";

function DocumentItem({ document, threadId }) {
  const [expanded, setExpanded] = useState(false);
  const [explanationVisible, setExplanationVisible] = useState(false);

  const handleToggleExpand = () => {
    setExpanded(!expanded);
  };

  const handleToggleExplanation = () => {
    setExplanationVisible(!explanationVisible);
  };

  return (
    <Paper sx={{ mb: 0, overflow: "hidden" }}>
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          p: 0,
          bgcolor: "background.paper",
        }}
      >
        <Box sx={{ flex: 1, minWidth: 0 }}>
          <Link
            href={document.metadata.url}
            target="_blank"
            rel="noopener"
            sx={{
              textDecoration: "none",
              color: "primary.main",
            }}
          >
            <Typography
              variant="subtitle2"
              sx={{
                fontWeight: "bold",
                fontSize: "0.75rem",
                overflow: "hidden",
                textOverflow: "ellipsis",
                whiteSpace: "nowrap",
                color: "text.secondary",
                "&:hover": {
                  color: "primary.main",
                },
              }}
            >
              {document.metadata.title || "Untitled"}
            </Typography>
          </Link>
        </Box>
        <IconButton onClick={handleToggleExpand} size="small">
          <ExpandMoreIcon
            sx={{
              color: "secondary.light",
              transform: expanded ? "rotate(180deg)" : "rotate(0deg)",
              transition: "transform 0.3s",
            }}
          />
        </IconButton>
        <Tooltip
          title={explanationVisible ? "Hide Explanation" : "Show Explanation"}
        >
          <IconButton onClick={handleToggleExplanation} size="small">
            {explanationVisible ? (
              <CloseIcon sx={{ color: "error.main" }} fontSize="small" />
            ) : (
              <HelpOutlineIcon sx={{ color: "info.dark" }} fontSize="small" />
            )}
          </IconButton>
        </Tooltip>
      </Box>
      <Collapse in={expanded}>
        <Box sx={{ p: 0.5, bgcolor: "background.paper" }}>
          <Typography
            variant="body2"
            sx={{
              color: "text.secondary",
              fontSize: "0.75rem",
              mb: 0.5,
              overflow: "hidden",
              textOverflow: "ellipsis",
              display: "-webkit-box",
              WebkitLineClamp: 10,
              WebkitBoxOrient: "vertical",
            }}
          >
            {document.page_content || "No preview available."}
          </Typography>
          <Typography
            variant="caption"
            sx={{
              mb: 0.5,
              color: "text.disabled",
              fontStyle: "italic",
            }}
          >
            {`Created: ${new Date(document.metadata.date_created).toLocaleDateString()}`}
          </Typography>
        </Box>
      </Collapse>
      {explanationVisible && (
        <Box sx={{ p: 0.5, bgcolor: "background.paper" }}>
          <ExplanationBox
            documentId={document.originalIndex}
            threadId={threadId}
          />
        </Box>
      )}
    </Paper>
  );
}

export default DocumentItem;
