import React, { useState } from "react";
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Divider,
  IconButton,
  Link,
  CircularProgress,
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import HelpOutlineIcon from "@mui/icons-material/HelpOutline"; // Icon for explanations
import CloseIcon from "@mui/icons-material/Close"; // Icon to close explanation
import axios from "axios";

function ResultsGrid({ results, threadId }) {
  const [expandedDocs, setExpandedDocs] = useState({});
  const [pageIndices, setPageIndices] = useState({});
  const [explanations, setExplanations] = useState({});
  const [loadingExplanation, setLoadingExplanation] = useState({});
  const [explanationVisible, setExplanationVisible] = useState({}); // Track visibility of explanations

  const handleToggleExpand = (source, index) => {
    setExpandedDocs((prev) => ({
      ...prev,
      [`${source}-${index}`]: !prev[`${source}-${index}`],
    }));
  };

  const handlePageChange = (source, direction) => {
    setPageIndices((prev) => ({
      ...prev,
      [source]: Math.max(
        0,
        Math.min(
          results[source].length - 4,
          (prev[source] || 0) + direction * 4,
        ),
      ),
    }));
  };

  const handleFetchExplanation = async (originalIndex) => {
    if (explanationVisible[originalIndex]) {
      setExplanationVisible((prev) => ({
        ...prev,
        [originalIndex]: false,
      }));
      return;
    }

    setExplanationVisible((prev) => ({
      ...prev,
      [originalIndex]: true,
    }));

    if (explanations[`${threadId}-${originalIndex}`]) return;

    setLoadingExplanation((prev) => ({
      ...prev,
      [originalIndex]: true,
    }));

    try {
      const response = await axios.get(
        `http://localhost:8000/explain/${threadId}?docid=${originalIndex}`,
      );
      setExplanations((prev) => ({
        ...prev,
        [`${threadId}-${originalIndex}`]: response.data,
      }));
    } catch (error) {
      console.error("Error fetching explanation:", error);
    } finally {
      setLoadingExplanation((prev) => ({
        ...prev,
        [originalIndex]: false,
      }));
    }
  };

  if (!results || Object.keys(results).length === 0) {
    return (
      <Typography variant="h6" sx={{ p: 2 }}>
        No results found.
      </Typography>
    );
  }

  return (
    <Box sx={{ p: 2 }}>
      <Grid container spacing={3}>
        {Object.keys(results).map((source, idx) => (
          <Grid item xs={12} sm={6} md={6} key={idx}>
            <Card
              sx={{
                borderRadius: 2,
                boxShadow: 3,
                overflow: "hidden",
                display: "flex",
                flexDirection: "column",
                height: "auto",
                bgcolor: "background.paper",
                transition: "transform 0.2s, box-shadow 0.2s", // Smooth transition on hover
                "&:hover": {
                  transform: "translateY(-4px)", // Lift card slightly on hover
                  boxShadow: 6,
                },
              }}
            >
              <CardContent
                sx={{
                  display: "flex",
                  flexDirection: "column",
                  height: "100%",
                }}
              >
                <Box
                  sx={{
                    display: "flex",
                    justifyContent: "space-between",
                    p: 1,
                  }}
                >
                  <IconButton
                    onClick={() => handlePageChange(source, -1)}
                    disabled={(pageIndices[source] || 0) === 0}
                    sx={{
                      color: "text.secondary",
                      "&:hover": {
                        color: "text.primary",
                      },
                    }}
                  >
                    <ChevronLeftIcon />
                  </IconButton>
                  <Typography
                    variant="h6"
                    gutterBottom
                    sx={{
                      textAlign: "center",
                      mb: 0,
                      fontWeight: "bold",
                      fontSize: "1.2rem",
                      color: "text.secondary",
                    }}
                  >
                    {source}
                  </Typography>
                  <IconButton
                    onClick={() => handlePageChange(source, 1)}
                    disabled={
                      (pageIndices[source] || 0) + 4 >= results[source].length
                    }
                    sx={{
                      color: "text.secondary",
                      "&:hover": {
                        color: "text.primary",
                      },
                    }}
                  >
                    <ChevronRightIcon />
                  </IconButton>
                </Box>
                {results[source]
                  .slice(
                    pageIndices[source] || 0,
                    (pageIndices[source] || 0) + 4,
                  )
                  .map((document, index) => (
                    <Box key={index} sx={{ mb: 2 }}>
                      <Box
                        sx={{ display: "flex", alignItems: "center", mb: 1 }}
                      >
                        <Link
                          href={document.metadata.url}
                          target="_blank"
                          rel="noopener"
                          sx={{
                            textDecoration: "none",
                            flex: 1,
                            "&:hover": {
                              textDecoration: "underline",
                            },
                          }}
                        >
                          <Typography
                            variant="body1"
                            sx={{
                              fontSize: "0.9rem",
                              fontWeight: "bold",
                              overflow: "hidden",
                              textOverflow: "ellipsis",
                              color: "text.primary",
                            }}
                          >
                            {document.metadata.title || "Untitled"}
                          </Typography>
                        </Link>
                        <IconButton
                          onClick={() => handleToggleExpand(source, index)}
                          sx={{
                            ml: 1,
                            color: expandedDocs[`${source}-${index}`]
                              ? "primary.main"
                              : "text.primary",
                            fontSize: "1rem",
                            transition: "color 0.3s",
                            "&:hover": {
                              color: "primary.dark",
                            },
                          }}
                        >
                          <ExpandMoreIcon
                            sx={{
                              transform: expandedDocs[`${source}-${index}`]
                                ? "rotate(180deg)"
                                : "rotate(0deg)",
                              transition: "transform 0.3s",
                            }}
                          />
                        </IconButton>
                        <IconButton
                          onClick={() =>
                            handleFetchExplanation(document.originalIndex)
                          }
                          sx={{
                            ml: 1,
                            color: explanationVisible[document.originalIndex]
                              ? "error.main"
                              : "info.main",
                            fontSize: "1.2rem",
                            transition: "color 0.3s",
                            "&:hover": {
                              color: explanationVisible[document.originalIndex]
                                ? "error.dark"
                                : "info.dark",
                            },
                          }}
                        >
                          {explanationVisible[document.originalIndex] ? (
                            <CloseIcon />
                          ) : (
                            <HelpOutlineIcon />
                          )}
                        </IconButton>
                      </Box>
                      <Box
                        sx={{
                          maxHeight: expandedDocs[`${source}-${index}`]
                            ? "none"
                            : "5em",
                          overflow: "hidden",
                          transition: "max-height 0.3s ease",
                          position: "relative",
                        }}
                      >
                        <Typography
                          variant="body2"
                          sx={{
                            fontSize: "0.85rem",
                            color: "text.secondary",
                            backgroundColor: "background.default",
                            p: 2,
                            borderRadius: 1,
                            maxHeight: expandedDocs[`${source}-${index}`]
                              ? "none"
                              : "calc(1.25em * 10)",
                            overflow: "hidden",
                            textOverflow: "ellipsis",
                            whiteSpace: "normal",
                            scrollbarWidth: "none",
                            msOverflowStyle: "none",
                            "&::-webkit-scrollbar": {
                              display: "none",
                            },
                            textAlign: "justify",
                            lineHeight: "1.6",
                          }}
                        >
                          {/* Conditionally render page_content based on its starting text */}
                          {document.page_content?.startsWith("Dataset Title:")
                            ? document.page_content.slice(
                                document.metadata.title.length + 15,
                                50000,
                              )
                            : document.page_content || "No preview available."}
                        </Typography>
                      </Box>
                      {/* Explanation Box */}
                      {explanationVisible[document.originalIndex] && (
                        <Box
                          sx={{
                            mt: 2,
                            p: 2,
                            borderRadius: 1,
                            bgcolor: "info.light",
                            color: "info.contrastText",
                            border: "1px solid",
                            borderColor: "info.dark",
                            overflowY: "auto",
                            textAlign: "justify",
                            scrollbarWidth: "none",
                            msOverflowStyle: "none",
                            "&::-webkit-scrollbar": {
                              display: "none",
                            },
                            position: "relative",
                          }}
                        >
                          <Typography
                            variant="subtitle2"
                            sx={{ mb: 1, fontWeight: "bold" }}
                          >
                            Explanation
                          </Typography>
                          {loadingExplanation[document.originalIndex] ? (
                            <Box
                              sx={{
                                display: "flex",
                                justifyContent: "center",
                                alignItems: "center",
                                height: "100%",
                              }}
                            >
                              <CircularProgress size={20} color="inherit" />
                            </Box>
                          ) : (
                            <Typography
                              variant="body2"
                              sx={{ fontSize: "0.85rem", lineHeight: "1.6" }}
                            >
                              {explanations[
                                `${threadId}-${document.originalIndex}`
                              ]?.generation || "No explanation available."}
                            </Typography>
                          )}
                        </Box>
                      )}
                      <Divider sx={{ my: 1 }} />
                    </Box>
                  ))}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

export default ResultsGrid;
